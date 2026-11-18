# Guía 3 — Bot centinela programado

**Objetivo:** un Bot dueño de una comprobación de calidad recurrente — la ejecuta en horario, tria fallos, los rastrea hasta la causa y envía correcciones.
**Nivel:** intermedio
**Implantación de origen:** el **Layout Bot** de Cognition — vigila regresiones de layout-shift en la app web de Devin. Cada 3 horas compila el `main` de producción, simula visitas de primera/repetida/peticiones retrasadas, y envía correcciones. **159 PRs en 3 semanas; lag −70%.**
**Fuentes:** [post de lanzamiento](https://devin.ai/blog/introducing-devin-bots) · [docs de Automations](https://docs.devin.ai/product-guides/automations)

## El patrón

Algunos trabajos nunca terminan — recurren en el reloj: presupuestos de rendimiento, regresión visual, frescura de dependencias, escaneos de secretos, uptime. Un Bot centinela es dueño *de la propia comprobación*, no solo de las correcciones: mantiene la comprobación funcionando conforme cambia el código, filtra ruido y solo abre una corrección cuando la regresión es real.

```text
cron ──► el Bot despierta ──► ejecuta la comprobación en condiciones realistas
                                   │
                      pass ────────┴──────── fail
                       │                         │
                     silencio       reejecuta para filtrar flakes
                                            │
                                   rastrea hasta el PR que la introdujo
                                            │
                               PR de corrección + evidencia antes/después
```

## Prerequisitos

- Una comprobación que pueda correr en la máquina del Bot (build, suite de tests, Lighthouse, script propio)
- Devin Bot creado (Guía 1) o una Automation (Guía 6) — ambos funcionan; un Bot añade juicio entre ejecuciones

## Paso 1 — El prompt de resultado

Reconstruido del comportamiento documentado del Layout Bot:

```text
Your job is to keep <surface> from <regressing>.

Watch <check/channel>, where <the check> posts every <interval>. Take over
that check and keep it working as the code changes. When something
regresses: rerun to rule out flakiness, trace the regression to the PR
that introduced it, and open a fix PR with before/after evidence.
```

Ejemplos para el slot `<check>`, todos vistos en implantaciones reales:

- medición de layout-shift en peticiones primeras/repetidas/retrasadas (Layout Bot)
- latencia p95 en tus 5 endpoints más lentos (plantilla Latency Optimizer)
- barrido `npm audit`/CVE (plantilla Code Health Engineer)
- detección de código muerto (plantilla Code Reaper)

## Paso 2 — Programarlo

Pídeselo al Bot en el chat:

```text
Run this check every 3 hours on a schedule.
```

El Bot propone una automatización; apruebas una vez. (La Guía 6 cubre automatizaciones hechas a mano si prefieres cablear el cron tú mismo.) Gestiónala después en Settings → Automations del Bot.

## Paso 3 — Las condiciones realistas importan

La comprobación del Layout Bot no es una ejecución — simula **primera visita, visita repetida y peticiones individualmente retrasadas**, porque la regresión que caza solo aparece bajo formas de carga específicas. Codifica tu equivalente:

- Qué entorno — el Bot compila el `main` de producción en su propia VM, no un dev server
- Qué inputs — caché fría vs. caliente, datos sembrados, orden realista de peticiones
- Qué umbral — un número, no "se siente más lento"

## Paso 4 — Disciplina de ruido

Dos reglas evitan que un centinela grite lobo:

1. **Reejecutar antes de actuar** — el Layout Bot reejecuta resultados que parecen flaky antes de tratarlos como reales. Escríbelo en el prompt: *"rerun any failed check once before acting on it."*
2. **Rastrear antes de corregir** — cada regresión se rastrea hasta el PR que la introdujo. Una corrección sin causa es una suposición.

## Paso 5 — Evidencia en cada corrección

Cada uno de los 159 PRs lleva **vídeo antes/después**. Evidencia equivalente para tu comprobación:

| Comprobación | Evidencia en el PR de corrección |
| --- | --- |
| Layout/visual | Grabación de pantalla o screenshots, antes vs. después |
| Latencia | Números de tiempo, misma medición en ambos sentidos |
| Código muerto | Por qué el código es inalcanzable |
| Dependencias/CVEs | El advisory + el diff que lo resuelve |

## Checklist de verificación

- [ ] La automatización existe y se dispara en el cron definido (Settings → Automations muestra ejecuciones)
- [ ] Una regresión sembrada produce un PR de corrección con evidencia antes/después
- [ ] Una ejecución flaky produce una reejecución, no una corrección
- [ ] La propia comprobación se mantiene — cuando la app cambió debajo de ella, el Bot actualizó la comprobación

## Trampas

- **Ser dueño de las correcciones pero no de la comprobación.** Si tu comprobación se rompe y nadie lo nota en una semana, el Bot era dueño de lo incorrecto — el prompt debe asignar la propia comprobación.
- **Cron sin juicio.** Una automatización programada simple puede ejecutar la comprobación; un Bot decide si el fallo es real. Usa automatización simple solo para comprobaciones sin triaje (Guía 6).
- **Salida solo de alerta.** Un centinela que reporta "regresión encontrada" a un canal crea trabajo para humanos. El valor de la implantación es que *corrige* — exígeselo.

## Prueba de conocimiento

1. ¿Por qué el centinela compila el `main` de producción en cron en lugar de esperar a que reporten fallos? *(El resultado es "sin regresiones", no "arreglar bugs reportados" — ser dueño significa encontrar problemas antes que los humanos.)*
2. El Layout Bot envía correcciones con vídeos antes/después — ¿qué decisión habilita eso para el revisor? *(Confianza para mergear sin reproducir localmente; la prueba viaja con el PR.)*
3. ¿Por qué rastrear una regresión hasta el PR que la introdujo en lugar de corregir el síntoma? *(Ser dueño de una comprobación es ser dueño de su historia — la corrección cae en la causa y el conocimiento persiste.)*

## Fuentes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — mecánica y números del Layout Bot
- [Automations — docs](https://docs.devin.ai/product-guides/automations) — programaciones, triggers, condiciones
- Relacionado: [Guía 6 — Automatizaciones orientadas a eventos](automations-101-event-driven.md) para la versión sin Bot de este bucle
