# Guía 15 — Living evals a partir de trazas de producción

**Objetivo:** una suite de evals para *tu* agente que se escribe sola — un Devin programado que lee conversaciones reales de producción, reconstruye cada fallo en una copia completa de tu sistema y abre PRs que añaden el fallo como test de regresión.
**Nivel:** avanzado
**Implantación de origen:** **Living Evals de Rox** — nadie en Rox escribe evals a mano ya. Un Devin semanal lee trazas de producción en Braintrust, reconstruye cada fallo en una copia completa de Rox sembrada con datos sintéticos, repite el request hasta que el agente comete el mismo error y abre un PR. La suite cubre **72% del uso real vs. 43–57%** de sus evals escritos a mano, y sigue creciendo semana a semana.
**Fuentes:** [write-up Living Evals](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) (Brian Xu, oct 2026) · [hilo de lanzamiento](https://x.com/rox_ai/status/2110779380666617997)

## El patrón

```text
trazas de producción (plataforma de observabilidad)
        │  muestra semanal (~350 conversaciones)
        ▼
agrupar en comportamientos (goal · output · mutation · target)
        │  cientos de conversaciones → ~130 comportamientos
        ▼
para cada comportamiento sub-cubierto:
   sintetizar datos → preview env de copia completa → replay del request
   → comparar con la traza de producción → congelar como eval → abrir PR
        ▼
el humano revisa el PR, no la escritura del eval
```

## Prerequisitos

- Un agente o feature de IA en producción, con **tracing a nivel de conversación** (Rox usó Braintrust; LangSmith/logging self-hosted funciona — necesitas el request + los registros + las tool calls tocadas)
- Una copia desplegable de tu sistema (preview env, staging o `docker compose up` en una VM) — **no mocks**
- Tests-como-código en tu repo para que un eval sea solo un archivo commitado

## Paso 1 — Haz una traza replayable a mano

Antes de programar nada: elige una conversación real donde tu agente falló. Pídele a Devin que traiga la traza, escriba datos sintéticos cubriendo exactamente lo que el request tocó, levante tu copia del sistema y repita el request hasta que ocurra el mismo fallo. Si no puedes reproducir un fallo manualmente, el bucle semanal no producirá nada.

## Paso 2 — Congélalo como eval, no como bug report

El artefacto es un eval commitado, no un mensaje de Slack. Convención de Rox: el request se copia **palabra por palabra** de producción; los datos sembrados reproducen las condiciones exactas (ej.: "la reunión más nueva no tiene transcripción"). Los requests que cambian datos obtienen una aserción de código; los de solo respuesta obtienen una rúbrica de LLM-judge.

## Paso 3 — Agrupa por comportamiento antes de escalar

Correr el bucle en cada conversación es despilfarro — la mayoría de los requests repite las mismas formas. Las cuatro etiquetas de Rox definen un *comportamiento*: **goal** (lo que el usuario quiere) · **output** (lo que vuelve) · **mutation** (nada/crear/editar/enviar) · **target** (objeto nombrado vs. inferido). ~350 conversaciones por semana colapsan a ~130 comportamientos; construye evals solo para comportamientos sub-cubiertos.

## Paso 4 — Codifica el procedimiento entero como un skill

El bucle traza→eval vive en **un archivo de skill** que Devin sigue: traer traza → sintetizar → preview env → replay → comparar → congelar → PR. Cuando el bucle produce un eval malo, **corrige el skill**, nunca parchees el eval a mano — esa es la jugada que se compone.

## Paso 5 — Prográmalo semanalmente

Automatización cron (Guía 6): traer las trazas de la semana → agrupar → por cada comportamiento sub-cubierto correr el bucle → abrir un PR con los nuevos evals. Los humanos revisan el PR; Devin es dueño de la suite.

## Checklist de verificación

- [ ] Un fallo real de producción se repite determinísticamente en tu preview env — mismo request del usuario, mismo mal resultado
- [ ] El archivo de eval está en tu repo, corre en CI y falla en el comportamiento viejo / pasa en la corrección
- [ ] La cobertura se mide contra el *mix de tráfico de producción*, no tus suposiciones — repórtala como el 72% de Rox
- [ ] Un eval malo se corrigió editando el skill, no el eval

## Trampas

- **Replay mockeado.** El enfoque anterior de Rox repetía a través de una capa de datos mockeada — los mocks pueden esconder bugs justo en el código que reemplazan. Usa una copia completa; el punto de un preview env es fidelidad.
- **Juicio flakey.** Incluso sin cambio de código, ~1 de cada 8 evals pasa en unas ejecuciones y falla en otras — los agentes no son determinísticos. Lee un fallo antes de confiar en él; no alertes en flakes aislados.
- **Evals midiendo gusto.** La suite caza regresiones comportamentales (un camino de tool muerto, un request soportado sin manejar), no estilo — cada fallo debe apuntar a un defecto corregible.

## Prueba de conocimiento

1. ¿Por qué repetir en una copia completa en vez de una capa de datos mockeada? *(Los mocks pueden esconder bugs en el código que reemplazan — a medida que el agente edita más estado, el mock se convierte en lo que realmente estás testeando.)*
2. ¿Por qué agrupar conversaciones en comportamientos antes de escribir evals? *(La mayoría de los requests repite formas — etiquetar goal/output/mutation/target permite que un eval cubra muchas conversaciones, así la cobertura mapea al uso real.)*
3. ¿Cuál es la jugada que se compone: corregir evals o corregir el skill? *(El skill — un eval parcheado a mano no le enseña nada a Devin; un skill corregido produce mejores evals para siempre.)*

## Fuentes

- [Living Evals: an eval suite that grows from production](https://www.rox.com/articles/living-evals-an-eval-suite-that-grows-from-production) — la metodología completa
- [Hilo de lanzamiento de Rox](https://x.com/rox_ai/status/2110779380666617997)
- Relacionado: [Guía 13 — Recetario oficial](official-cookbook.md) · [Guía 6 — Automatizaciones](automations-101-event-driven.md)
