# Guía 4 — Organización multi-Bot

**Objetivo:** una jerarquía de Bots que opera una unidad de negocio entera — un orquestador delegando a Bots especialistas, un humano decidiendo a través de un único hilo diario.
**Nivel:** avanzado
**Implantación de origen:** el **SuperJennyStack** de Jenny Xu — ~20 Bots operando un estudio de juegos móviles. ~50 → **1.900 PRs/semana**, releases semanales, ingresos del estudio ×6. Publicado como plantilla comunitaria en el [Bot marketplace](https://devin.ai/bots/templates). El **handoff por grant bot-a-bot** oficial (QA → Developer → retest → informe del PM) usa la misma mecánica a menor escala.
**Fuentes:** stack publicado de Jenny Xu ([vía cobertura del lanzamiento](https://x.com/cognition/status/2122737511684587551)) · [docs de Bots](https://docs.devin.ai/work-with-devin/bots) · [post de BotSpeak](https://x.com/xujennyc/status/2123111543105868166)

## El patrón

No construyas un Bot que hace todo — construye una pequeña empresa:

```text
                    ┌─────────────┐
              ┌────►│ Orquestador  │◄──── un hilo consolidado
              │     └──────┬──────┘      (4×/día, respuestas emoji)
              │            │ grants: lectura + mensaje
     ┌────────┼────────┬───┴─────┬──────────┐
     ▼        ▼        ▼         ▼          ▼
  SuperPM  SuperDev  SuperQA  SuperRelease  SuperSupport
  (el qué) (construye)(verifica)(envía)    (usuarios)
```

El humano es el CEO: el orquestador recoge todas las decisiones pendientes de los Bots subordinados en **un hilo de Slack, 4×/día**, respondido con emoji.

## Prerequisitos

- Guía 1 hecha — sabes crear e instruir un Bot
- Slack conectado — este patrón vive en Slack; el hilo consolidado del orquestador es toda la UX
- Un dominio acotado con trabajos separables (un producto, un estudio, un área de servicio)

## Paso 1 — Diseña el organigrama primero

El stack publicado de Jenny — copia la *forma*, no los nombres:

| Bot | Posee |
| --- | --- |
| Orquestador (SuperJenny) | Delegación a todos los demás Bots; compila sus peticiones en un hilo; entrenado en su personalidad/modos |
| PM (SuperPM) | Lista diaria rankeada de correcciones desde métricas + reseñas de tienda + tendencias |
| Release (SuperRelease) | Build semanal, listo para envío a la tienda el viernes |
| QA (SuperQA) | Tests en dispositivo real con prueba en vídeo |
| Support (SuperSupport) | Redacta cada respuesta a reseñas de tienda para aprobación; ayuda a jugadores de noche |

Los ~15 Bots restantes cubren desarrollo, Unity, UI, iOS, Android, analytics. Regla práctica de la implantación: **un Bot por puesto que nombrarías en un organigrama** — no por tarea, por *responsabilidad*.

## Paso 2 — Crea los especialistas

Para cada puesto, un Bot con prompt de resultado acotado:

```text
You own QA for <product>. Test every release candidate on real devices,
post video proof, and block release on failures. Report what needs a
decision to the orchestrator.
```

Mantén las Instructions de cada Bot enfocadas en las reglas de su puesto; el conocimiento compartido (marca, proceso de deploy, quién aprueba qué) va en las instructions de cada Bot o en un recurso compartido — no hay memoria global entre Bots, así que los prompts del orquestador cargan el tejido conectivo.

## Paso 3 — Cablea los grants

Un grant da al Bot A acceso de lectura/mensaje al Bot B — así es como los Bots se pasan trabajo entre sí (los Bots piden el grant; tú apruebas la tarjeta una vez). El orquestador necesita acceso a todos los especialistas.

La variante oficial documentada — más pequeña, misma mecánica:

```text
QA Bot encuentra un bug ──grant──► Developer Bot lo arregla ──► QA retestea en
staging ──► PM Bot reporta estado en el canal
```

Aprueba grants de forma estrecha: el orquestador lee y manda mensajes a los especialistas; los especialistas no necesitan todos alcanzarse entre sí.

## Paso 4 — El hilo consolidado

Esta es la instrucción más importante — convierte interrupciones de 20 Bots en un solo hábito:

```text
Collect every pending decision from the Bots you work with into one
Slack thread, posted at <times> daily. For each item: what's blocked,
the options, your recommendation. I answer in replies/emoji; treat my
replies as decisions and relay them.
```

Jenny lo ejecuta **4×/día** y responde **con emoji**. La disciplina: nunca hablas con los especialistas — el orquestador retransmite tu decisión y la lleva hasta el final.

## Paso 5 — Cadencia = el latido de la org

| Cadencia | Quién la ejecuta |
| --- | --- |
| Lista diaria rankeada de correcciones | Bot PM (métricas + reseñas + tendencias) |
| Release candidate semanal | Bot Release → sign-off del Bot QA |
| Hilo de decisiones 4×/día | Orquestador |
| Ayuda a jugadores de noche | Bot Support (redacta respuestas para aprobación matinal) |

Cada Bot es dueño de su bucle; el orquestador es dueño del calendario de bucles.

## Paso 6 — Protocolo inter-bot (BotSpeak)

El problema de escala que nadie te advierte: los 20+ Bots de Jenny enviaban **700+ mensajes/día** — ella no podía seguir el ritmo. Su corrección fue **BotSpeak**, una taquigrafía que ahorra tokens y que los Bots usan *entre sí* ([su relato](https://x.com/xujennyc/status/2123111543105868166)):

| Regla | Qué significa |
| --- | --- |
| Abreviaturas | `ACK` y afines en vez de respuestas completas |
| ASD-STE100 | Gramática inglesa simplificada — el estándar de documentación aeronáutica, sin ambigüedad y barato en tokens |
| Recibos emoji | Reaccionar ✅ en vez de "entendido, gracias" |
| Sin cortesías | Los Bots se mandan entre sí solo lo que el otro necesita |
| El humano recibe prosa | El hilo consolidado sigue en frases completas con contexto de decisión |

Seis días después del cambio: decisiones tomadas por Bots sin ella **×12**, peticiones repetidas −50%, posts de aclaración entre bots −12%. El protocolo existe porque el desperdicio de tokens no es el coste real — el desperdicio de *atención* lo es: mensajes bot-a-bot más cortos mantienen legible el único hilo del humano.

## Checklist de verificación

- [ ] Cada Bot especialista tiene prompt de resultado acotado y grants activos
- [ ] El orquestador publica el hilo de decisiones consolidado en horario
- [ ] Una decisión que respondiste por emoji fue retransmitida y resuelta por el especialista correcto
- [ ] Un handoff entre Bots se completó de punta a punta (encontrar → arreglar → verificar → reportar)
- [ ] Mensajes humanos de hoy < número de PRs mergeados

## Trampas

- **Saltarse el orquestador.** N Bots cada uno mandándote DM es N× ruido. La org solo funciona si el juicio se canaliza por un hilo.
- **Fronteras de puesto vagas.** "Dev Bot" y "Fix Bot" colisionarán. Las fronteras siguen el organigrama — QA *verifica*, Release *envía*, PM *prioriza*.
- **Over-granting.** Grants en malla (todos alcanzan a todos) recrean el caos. Hub-and-spoke a través del orquestador.
- **Prosa entre Bots.** Bots escribiéndose párrafos entre sí es cómo se llega a 700 mensajes/día — adopta un protocolo estilo BotSpeak: abreviaturas + recibos emoji + sin cortesías; frases completas solo para el humano.

## Prueba de conocimiento

1. ¿Por qué SuperJennyStack enruta todo el contacto humano por *un* hilo consolidado? *(La atención es el cuello de botella, no el cómputo — 20 Bots generando 20 hilos son 20 empleos otra vez.)*
2. ¿Cuándo un grant vence a "preguntar al orquestador"? *(Cuando la capacidad necesaria ya la posee otro Bot — los grants toman prestada propiedad en vez de duplicarla.)*
3. ¿Qué implica la cadencia "4×/día con emoji" del humano sobre la profundidad de la delegación? *(Ancho de banda de decisión, no plantilla, es lo que los Bots reemplazan — el humano conservó la capa de juicio y perdió la capa de tecleo.)*

## Fuentes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — números de SuperJennyStack, variante grant-handoff
- [Bot marketplace](https://devin.ai/bots/templates) — plantilla comunitaria SuperJennyStack + 16 plantillas oficiales
- [Docs de Bots](https://docs.devin.ai/work-with-devin/bots) — grants, memoria, acceso
- Relacionado: [Guía 5 — Enjambre anclado en referencia](bots-204-reference-grounded-swarm.md) para enjambres que *escriben* en vez de *operar*
