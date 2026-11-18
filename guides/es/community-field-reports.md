# Guía 14 — Informes de campo de la comunidad

**Objetivo:** lo que los ingenieros que corrieron Devin en trabajo real aprendieron — incluyendo los fracasos. Destilado de relatos hands-on publicados, tanto elogiosos como hostiles.
**Nivel:** empieza aquí para juicio
**Fuentes:** enlazadas por informe abajo

Esta guía es deliberadamente equilibrada: dónde Devin gana con fiabilidad, dónde quema dinero, y el estilo de trabajo que separa los dos resultados.

## El patrón que se repite en todo informe

Los usuarios que obtienen resultados tratan a Devin como un **ingeniero júnior asíncrono**, no un generador de código. Scott Wu (CEO de Cognition) describe el workflow interno en [Lenny's Newsletter](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers): delegar tareas bien acotadas, dejarlas correr mientras haces reuniones, revisar PRs. [El relato de Every](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent) llega al mismo encuadre — exige un *skill set*: aprender en qué es bueno, escribir tareas que entiende, saber cuándo intervenir, y aprender a confiar en trabajo hecho distinto al tuyo.

## Dónde Devin ganó, documentado

**Prototipado de punta a punta.** Desde un repo en blanco, Devin scaffolded un "City Explorer" FastAPI + React (integraciones de imágenes/clima/noticias), lo corrió localmente, abrió un PR y desplegó una URL pública — ~90 minutos, ~2 intervenciones humanas ([hands-on en Medium](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)). [Scott Logic](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html) reporta el mismo arco en un prototipo de cliente real — con una lección crucial de iteración abajo.

**Trabajo que necesita un runtime.** En un [head-to-head con Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/), Devin perdió en tareas de ajustarse a tus convenciones pero ganó claramente donde una máquina ayuda: caza de memory leaks donde profiled, tomó heap snapshots bajo carga y produjo un informe — la VM propia del agente es la feature.

**Troubleshooting en vivo.** [Faros](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting) usó Devin *durante una llamada con cliente*: leyó el código de la introspection API y generó un `curl` funcional en segundos — colapsando un bucle de seguimiento de 1–2 días dentro de la propia llamada.

**Migraciones reales con docs frescas.** Un upgrade Tailwind 3→4 + DaisyUI 4→5 en un codebase Vue→React complicado funcionó cuando el equipo alimentó a Devin con docs actuales vía el MCP Context7 — el prompt llevaba el *contexto*, no solo la tarea ([write-up en Bootcamp](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)).

**Auto-verificación.** Una [comparación de practicante de un año](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying) marca el e2e testing dirigido por navegador de Devin como el momento umbral: navega a lo que construyó y lo comprueba — un bucle de feedback que parece ingeniería, no generación.

**Más allá del código.** Un investigador de Cognition reporta que Devin reconstruyó — y terminó — una formalización en Lean que le tomó buena parte de un semestre nueve años antes, en **menos de 15 minutos** ([post](https://x.com/penlume/status/2115806616796921885)). La formalización matemática recompensa el mismo rasgo que las migraciones: una definición de hecho verificable por máquina.

**Cableado a observabilidad.** [Dynatrace MCP + Devin](https://medium.com/lets-code-future/how-i-turned-devin-into-a-performance-analysis-agent-with-dynatrace-mcp-753d3f4790a2) convierte a Devin en un agente de análisis de rendimiento: consulta métricas y trazas en vivo, luego diagnostica — el servidor MCP lleva contexto de producción que el repo no puede (Medium). Ver también [Devin: del bug report al pull request](https://medium.com/@winter.inc/devin-from-bug-report-to-pull-request-25-days-of-ai-day-18-b158daa20f23) para el bucle ticket→PR simple de punta a punta.

## Dónde falló, documentado

- **Prompts vagos o demasiado amplios.** El primer prompt de Scott Logic produjo un scaffold inutilizable; estrechar el stack y la petición ("just the models") lo arregló. Devin sobre-construye — dile qué *no* construir.
- **Tareas de ajuste a convenciones.** "Add pagination to this endpoint" volvió desalineado de las convenciones del codebase en dos informes independientes ([amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios), [mohitkhare](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)) — Devin construye en aislamiento a menos que lleves las convenciones hasta él (→ Guía 9).
- **Trabajo no verificable.** [expectedwrong](https://expectedwrong.com/devin-appraised) y el [test de 10 tareas de alanwest](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) documentan el modo de fallo: salida confiada que está rota o ausente, créditos quemados en bucles. Sus tareas se inclinaron a trabajo sin verificación clara — el mismo gate que el playbook oficial hace obligatorio (Guía 11).

## Implantaciones de equipos nombrados (comunidad, con números)

Orgs reales publicando sus datos operativos de Devin — mayoritariamente de la comunidad de ingeniería de Japón, que documenta excepcionalmente bien:

| Equipo | Implantación | Resultado reportado |
| --- | --- | --- |
| rakko_inc | Code review automático vía Playbooks + GitHub Actions + Devin API — pre-digiere cada PR antes de la revisión humana | **65 → 184 PRs revisados/mes (2.8×)**; los humanos parten del resumen de Devin ([informe](https://zenn.dev/rakko_inc/articles/00cc5a5a679971), JP) |
| Skillnote (QA) | PR → Actions → Devin genera borradores de diseño de tests (CSV/Excel, incl. "por qué este caso") publicados en el PR | ~**35 min ahorrados por 10 casos de prueba**; los casos diseñados por Devin pillaron bugs que los humanos perdieron ([informe](https://zenn.dev/skillnote/articles/5ba429ca249801), JP) |
| arufian | Automatización serverless de eventos GitHub (sin servidor fijo): labels `devin:fix`/`devin:plan` dirigen sesiones Devin, con **tabla de política prioridad × complejidad** y flujo de aprobación plan-first | Los safety scans hacen gate de PRs arriesgados; trabajo de alta complejidad obtiene plano → aprobación humana → `run that plan` ([informe](https://zenn.dev/arufian/articles/f80a62f5217cee), JP) |
| Leverages (levtech) | Rollout de org: 14 equipos / ~30 personas | **177 PRs mergeados** en ~2.5 meses; miden ROI como `coste ACU − horas ahorradas × salario` y siguen el mix por tipo de tarea ([informe](https://zenn.dev/levtech/articles/9c869303820844), JP) |
| Decagon | AutoResearch en Devin Cloud: un Devin orquestador + subagentes paralelos compitiendo hipótesis; cada idea verificada contra tráfico de producción replicado en GPUs de Modal | **hasta 2.5× más throughput por GPU** en el tráfico de soporte ([writeup](https://x.com/DecagonAI/article/2115511110120120437)) |
| Nader Dabit | Org personal de 5 bots — **CTO** (todas las sesiones/repos, iMessage VIP), **Auto(mation)Bot** (corre sus automatizaciones, informes de perf), **DevCommunityBot** (datos del programa de embajadores → mini-apps), **DevRelBot** (docs + vídeos-tutoriales con *su propio ordenador, cuentas propias de Devin/GitHub/Linear, clon de voz ElevenLabs*) | Más **Windfable**: ~10 Bots SuperJennyStack en un RPG iOS Unity, cada uno con macOS+Xcode+Unity propios, probando iPhone Duo en modos plegado/desplegado con diffs de screenshot/vídeo ([primer](https://x.com/dabit3/status/2122755275182469515)) |
| Mark Fenner | Operador en solitario corriendo cuatro Bots de cargos bajo un Chief Agent Bot coordinador ("Frankie") | Actualizaciones consolidadas en una superficie de decisión única — la forma multi-Bot funciona sin equipo ([walkthrough](https://x.com/markfenner/status/2122740244328145211)) |

Las ideas reutilizables dentro: **gating por tabla de política** (arufian: solo auto-PR trabajo de bajo riesgo, plan-first para lo complejo), **prompting de salida fija** (Skillnote: formato CSV fijo + Python inline para la conversión mata la varianza de la salida), **pre-digest para el revisor** (rakko: Devin resume + señala antes de que el humano lea) y **contabilidad honesta** (la fórmula ROI ACU-vs-salarios de levtech).

## Las lecciones destiladas

1. **Acota la porción, no el proyecto.** Los éxitos son todos unidades acotadas; los fracasos son "construye/arregla esto ampliamente." (Doctrina oficial: Guía 13.)
2. **Verifica o no delegues.** Dale a Devin trabajo donde una máquina pueda comprobar "hecho" — tests, builds, un `curl` funcional, una página renderizada.
3. **Lleva contexto, no suposiciones.** Convenciones, docs actuales (vía MCP), la forma de tu stack — los fracasos son fracasos de contexto, no de capacidad.
4. **Delega; no mires.** El ROI en todo informe positivo es *asincronía* — las tareas corren mientras haces otra cosa. Mirarlo teclear es cómo decides que es "lento".
5. **Itera el prompt, no la herramienta.** La corrección de Scott Logic no fue otro agente — fue un prompt más estrecho. Trata una primera ejecución fallida como un bug del prompt.

## El top-5 interno de Scott Wu (de la entrevista de Lenny's)

Las tareas que la propia Cognition más delega: **arreglos de frontend, upgrades de versión, documentación, respuesta a incidentes, testing** — más un patrón de "primera línea de defensa" donde Devin analiza crashes antes de que los humanos se activen, e investigación en DeepWiki para *escribir mejores prompts*.

## Checklist de verificación

- [ ] Elige el informe más cercano a tu stack y relee el original, no la destilación — ¿la cifra se sostiene en contexto?
- [ ] Escribe la única lección en la que apostarías dinero reproduciendo en tu org; si no puedes nombrarla, elige otro informe

## Trampas

- **Sesgo de supervivencia.** Los informes brillantes publican números; los fracasos silenciosos no publican nada. Lee los fracasos de esta colección como la experiencia mediana, las victorias como el techo.
- **Cargo cult.** La iteración de prompt de Scott Logic funcionó *porque* iteraron — copiar su prompt final sin su bucle te da su inicio, no su resultado.

## Prueba de conocimiento

1. ¿Qué tienen en común los informes de fracaso que los de éxito no tienen? *(Delegación no verificable — los fracasos dieron a Devin trabajo donde nadie podía comprobar "hecho"; todo éxito definió una comprobación.)*
2. ¿Por qué el "debugging en una llamada con cliente" de Faros es una lección de implantación, no una anécdota? *(Muestra la maniobra de triage en vivo: el agente como primer respondedor mientras el humano mantiene la relación con el cliente.)*
3. ¿Por qué esta guía cuenta un informe hostil como fuente en igualdad? *(Los informes adversariales sacan a la superficie las condiciones de frontera — aprendes los bordes del mapa de quienes salieron de ellos.)*

## Fuentes

- [Scott Logic — Rapid development with Devin](https://blog.scottlogic.com/2025/10/20/rapid-development-with-devin.html)
- [Lenny's Newsletter — Scott Wu on Cognition's internal Devin usage](https://www.lennysnewsletter.com/p/how-devin-replaces-your-junior-engineers)
- [Every — Coding with Devin](https://every.to/chain-of-thought/coding-with-devin-my-new-ai-programming-agent)
- [dev>notes — Devin vs Claude Code](https://web.archive.org/web/20260718112612/https://mohitkhare.me/blog/devin-vs-claude-code/)
- [Faros — Devin for live troubleshooting](https://www.faros.ai/blog/how-to-use-devin-ai-troubleshooting)
- [Medium — Copilot, Cursor or Devin weekend](https://medium.com/@sambhavgaur_70582/copilot-cursor-or-devin-my-hands-on-weekend-with-ai-that-codes-and-deploys-acc708e802b3)
- [Bootcamp — Day 7 with Devin (Tailwind/DaisyUI migration)](https://medium.com/design-bootcamp/day-7-of-30-getting-to-know-devon-ai-and-working-with-him-743c351cd0c4)
- [architect to CTO — The only coding agent worth paying for](https://architecttocto.substack.com/p/the-only-coding-agent-worth-paying)
- [expectedwrong — Devin, appraised](https://expectedwrong.com/devin-appraised) · [dev.to — 10 real tasks, 3 completed](https://dev.to/alanwest/i-gave-devin-10-real-tasks-it-completed-3-3063) · [amillionmonkeys](https://www.amillionmonkeys.co.uk/blog/ai-coding-tools-small-studios)
- [Signadot — Testing Devin's changes end to end](https://dev.to/signadot/test-devins-changes-end-to-end-with-signadot-a0)
