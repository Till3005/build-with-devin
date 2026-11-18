# Prompts de resultado para Bots, disecados

**Objetivo:** escribir prompts de resultado como los hicieron realmente las implantaciones documentadas — propiedad de un área, no una lista de tareas.
**Nivel:** intermedio · **Tiempo:** 20 min para redactar, una semana para calibrar

Toda implantación pública de bot que produjo números grandes empezó con un prompt corto que asignaba un *resultado*. Esta guía colecciona los reales y hace ingeniería inversa de por qué funcionan.

## El ejemplar

> *"your job is to product manage the android app"*

Toda la asignación del Android Bot. Una frase produjo 44 días de trabajo autodirigido: el bot descompuso el resultado en tickets que escribió él mismo, corrió una sesión Devin por ticket y entregó 1.134 PRs mergeados ([post de lanzamiento](https://devin.ai/blog/introducing-devin-bots)). Fíjate en lo que el prompt **no** contiene: sin lista de tickets, sin criterios de aceptación, sin agenda. El resultado en sí los implica todos.

## La anatomía de un prompt de resultado que funciona

| Elemento | Qué hace | Ejemplo |
| --- | --- | --- |
| **Un rol** | Le dice al bot cómo *comportarse*, no solo qué producir | "product manage", "own the QA of onboarding flows" |
| **Una superficie acotada** | Un alcance que el bot puede ver por completo — una app, una comprobación, una fuente de datos | "the android app", "layout regressions", "30+ onboarding flows" |
| **Una definición de hecho implícita** | Un estado contra el que el bot puede verificarse | "feature parity with iOS", "no layout-shift regressions", "every flow green" |
| **Autoridad permanente** | El bot decide *cuándo* y *qué después* — eso es lo que lo hace un bot, no un script | "your job is to…", "keep…", "watch for…" |

## Patrones del marketplace oficial de plantillas

Las 16 [plantillas del marketplace](https://devin.ai/bots/templates) siguen todas la misma gramática. Formulaciones reutilizables, generalizadas:

**Propiedad de un dominio** — "Find bugs, improvements, performance and refactoring work in a named product area; open one small PR at a time with proof it works." (Software Factory)

**Propiedad de una comprobación** — "Every 3 hours, build production main, simulate first/repeat/deferred visits, and file fixes with before/after videos for any regression you introduce—or find." (patrón Layout Bot)

**Propiedad de una etapa del ciclo de vida** — "Take a ticket or an ask to a tested PR and through review." (Product Engineer)

**Propiedad de una cadencia** — "Weekly: remove dead code, one safe PR per round." (Code Reaper) — los resultados programados se declaran como ritmo, no como disparador.

**Propiedad del metabolismo del equipo** — "Watch the channels, post updates, hand work to the right teammate, follow up until done." (Chief of Staff)

**Propiedad de la higiene** — "Old flags, stale deps, CVEs — turned into small safe PRs." (Code Health Engineer)

## Orgs multi-bot: prompts que conceden autoridad

En flotas (SuperJennyStack, Frankie, tigsbot) el prompt del bot jefe contiene el *contrato de enrutamiento*: qué bot posee qué superficie, y cuándo escalar hacia arriba en vez de hacia el lado. El verdadero prompt del humano es la spec del hilo consolidado: "bring me every open decision in one thread." Ver la [Guía 4](bots-203-multi-bot-org.md) para el organigrama completo.

## Antipatrones

- **Prompts con forma de tarea.** "Fix these 12 issues" — el bot termina y queda ocioso; obtienes una sesión, no un bot.
- **Resultados no verificables.** "Make the app better" — sin autocomprobación, la única salida del bot es spam de Needs-you.
- **Alcance oculto.** Si el resultado requiere sistemas que el bot no ve (un staging al que no llega, un dashboard que no lee), o se atasca o alucina progreso. Dale la superficie o encoge el resultado.
- **Sin historia de autoridad de merge.** El 88% de auto-merge existe porque CI y gates de review estaban preconfigurados para merges autónomos. Decláralo: "merge when CI is green and diff < N lines" o "always open as draft for human review."

## Redactando el tuyo — la prueba de las tres líneas

Un buen prompt de resultado responde, en orden:

1. **¿Qué es tuyo?** — la superficie
2. **¿Cómo se ve "bien"?** — el estado verificable
3. **¿Qué haces al respecto?** — el comportamiento permanente

Si un extraño no pudiera comprobar la verdad de la línea 2 desde fuera, apriétala.

## Checklist de verificación

- [ ] Toma un ítem real del backlog de tu repo y reescríbelo como prompt de resultado — superficie, estado verificable, comportamiento permanente
- [ ] Muéstraselo a alguien que no conoce el codebase: ¿podría decir desde fuera cuándo el Bot está "ganando"?
- [ ] La primera respuesta del Bot debe ser un plan o preguntas de aclaración sobre el alcance — si pregunta "qué quieres que haga primero", el prompt no asignó propiedad

## Trampas

- **Una lista de tareas con disfraz de resultado.** "Do X, then Y, then Z" sigue siendo una checklist — el Bot no puede repriorizar cuando el mundo cambia.
- **"Keep the app good" sin definición de bueno.** Sin estado verificable, el Bot elige una — y no será la tuya.
- **Alcance más ancho que una superficie.** "Own engineering" falla; "own the iOS app" entrega. Divide por lo que un único extraño podría observar por completo.

## Prueba de conocimiento

1. ¿Por qué "own the Android app" funciona mejor que "fix Android bugs"? *(La propiedad implica juicio permanente — el Bot decide qué bugs importan, no solo si arreglar.)*
2. ¿Qué tiene de malo "make the CI fast"? *(No verificable desde fuera — sin umbral. "CI under 8 minutes" lo es.)*
3. ¿Cuál de las tres preguntas responde "text me if tests fail"? *(Comportamiento permanente — dice qué hace el Bot sobre el estado, nada sobre la superficie o la meta.)*

## Fuentes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Docs de Bots](https://docs.devin.ai/work-with-devin/bots) · [Marketplace de plantillas](https://devin.ai/bots/templates)
- Relatos de implantación enlazados en [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)
