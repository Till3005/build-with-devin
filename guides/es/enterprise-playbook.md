# Guía 7 — Patrones de rollout enterprise

**Objetivo:** desplegar Devin a escala organizacional usando las formas que ya produjeron números publicados — no experimentación, las maniobras probadas.
**Nivel:** intermedio (escrito para líderes de ingeniería)
**Fuente:** casos de clientes publicados, [devin.ai/customers](https://devin.ai/customers)

Seis formas de implantación, destiladas de las empresas que publicaron resultados. La mayoría de los rollouts exitosos usan dos o tres de ellas, no las seis.

## Forma 1 — El motor de migración de legado (Nubank, Comarch)

| | |
| --- | --- |
| Implantación | Nubank: monolito ETL de 8 años y millones de líneas → submódulos. Comarch: reconstrucción de ERP de 20 años y 10M líneas |
| Resultado | 8–12× eficiencia de ingeniería, 20× ahorro de coste (Nubank) |
| Mecanismo | Hacer fine-tune de Devin en *tu* codebase (Nubank bajó de ~40 min/tarea a ~10), luego apuntarlo a la migración como programa continuo — PRs pequeños rastreados, no una reescritura |

**Cómo copiarlo:** elige un sistema legado acotado; haz fine-tune o enséñalo vía playbook; ejecuta el loop estilo Migration Engineer — una gran migración como PRs pequeños rastreados con superficie de progreso. El beneficio se compone: cada módulo migrado hace más lista a la siguiente sesión.

## Forma 2 — El repo de autor primario (EBANX, Gumroad, Finch)

| | |
| --- | --- |
| Implantación | EBANX: **92% de los PRs mergeados con autoría de Devin**. Gumroad: Devin es el **contribuidor n.º 1** del repo (1.500+ PRs). Finch: 3.000 PRs, ~20 ingeniero-meses ahorrados |
| Mecanismo | Devin no es asistente en estos repos — es el autor por defecto. Los humanos revisan y dirigen |

**Cómo copiarlo:** elige un repo de alta velocidad; enruta tickets a sesiones Devin por defecto; los humanos revisan. La métrica a vigilar es la cuota de PRs de autoría — por encima de ~50%, estás en esta forma; por debajo, sigues en modo piloto.

## Forma 3 — El primer respondedor siempre activo (Modal, Reducto, AngelList)

| | |
| --- | --- |
| Implantación | Modal: **80% de los incidentes investigados antes de que un ingeniero abra el hilo**. Reducto: Devin Oncall es el primer respondedor; ingenieros rara vez paginados. AngelList: Devin encuentra la causa raíz del 70% de los incidentes antes del ingeniero |
| Mecanismo | Trigger PagerDuty/Slack → la sesión investiga con acceso a logs/repo → el informe cae antes de que el humano despierte |

**Cómo copiarlo:** [Devin Oncall](https://docs.devin.ai) o una automatización disparada por PagerDuty (Guía 6, receta: incidente → investigar). Mide el % de incidentes pre-investigados — cada punto de ello es sueño humano recuperado.

## Forma 4 — La flota de mantenimiento (Airbyte, Melius)

| | |
| --- | --- |
| Implantación | Airbyte: mantiene **700+ conectores** funcionando. Melius: ~100 PRs/día |
| Mecanismo | La larga cola que nadie quiere — podredumbre de conectores, deriva de dependencias, flags viejas — enrutada a Bots/automatizaciones que la procesan continuamente |

**Cómo copiarlo:** enumera tu backlog de mantenimiento (el trabajo que los ingenieros evitan); envuélvelo en Bots estilo Code Health Engineer / Code Reaper (plantillas oficiales) con cadencia semanal.

## Forma 5 — El seat para toda la org (Wayfair, The Access Group, Citi)

| | |
| --- | --- |
| Implantación | Wayfair: 1.600+ ingenieros all-in. Access Group: Devin en 250 productos, 2.000+ ingenieros → 5× output. Citi: rollout a 40.000 devs, 30% de recorte en gasto con proveedores tech |
| Mecanismo | No más agentes — el *seat*: cada ingeniero tiene acceso a Devin, playbooks compartidos, knowledge a nivel de org |

**Cómo copiarlo:** el orden de rollout en los casos publicados es consistente — equipo piloto → resultados medidos → estandarización de playbook/knowledge → expansión de seats. Saltarse el paso de knowledge es por lo que los rollouts de seats se atascan: ver la [guía de playbooks](playbooks-and-knowledge.md).

## Forma 6 — El gate de proceso (Hamming, Litera, Eight Sleep)

| | |
| --- | --- |
| Implantación | Hamming: Devin escribe el 25% del volumen de código. Litera: ciclos de regresión reducidos un 90%. Eight Sleep: 8× más entregado |
| Mecanismo | Devin posee una etapa del pipeline — tests de regresión, QA — no el producto entero |

**Cómo copiarlo:** encuentra la etapa del pipeline con peor coste humano (ciclos de regresión, QA); asígnala a un Bot o automatización; mide el tiempo de ciclo de la etapa antes/después.

## Antipatrones que los casos implican

- **Herramienta, no colega.** Las implantaciones de números altos dan a Devin propiedad (repos, superficies, etapas), no asignaciones — misma lección que las Guías 1–5.
- **Piloto eterno.** Todo resultado publicado comparte un rasgo: un piloto medido que *se graduó*. Define el criterio de graduación por adelantado (cuota de PRs, incidentes cubiertos, horas ahorradas).
- **Sin capa de knowledge.** Toda implantación grande codifica convenciones en algún sitio — fine-tunes, playbooks, instructions de Bot. Sin ello, la calidad varía por sesión.

## Checklist de verificación

- [ ] Tu doc de rollout nombra una etapa de pipeline, una métrica y un criterio de graduación — antes de la primera sesión
- [ ] Checkpoint de la semana 2: ¿puedes decir la cuota de PRs mergeados de Devin en esa etapa sin preguntar a nadie?

## Trampas

- **Escalar el piloto que nunca se graduó.** Todo número grande aquí llegó después de un piloto medido con criterio de salida.
- **Pensar primero en licencias.** Comprar seats antes de nombrar la etapa poseída produce shelfware — el patrón es etapa → piloto → métrica → entonces seats.

## Prueba de conocimiento

1. ¿Por qué las seis formas comparten "una etapa poseída" como átomo? *(Todo número publicado vino de una superficie acotada y medible — las orgs que desplegaron "en todas partes" no publicaron nada.)*
2. ¿Qué es el criterio de graduación y por qué fijarlo antes del piloto? *(Una métrica + umbral que pasa de piloto → producción; sin él, los pilotos derivan para siempre o mueren por sensaciones.)*
3. ¿Por qué la capa de knowledge aparece en toda implantación grande? *(La consistencia a escala requiere contexto compartido — la alternativa es N sesiones de distinta calidad.)*

## Fuentes

- [devin.ai/customers](https://devin.ai/customers) — todos los casos y números citados
- [built-with-devin — índice enterprise](https://github.com/Till3005/built-with-devin#enterprise-deployments) — la tabla de casos verificada del registry
