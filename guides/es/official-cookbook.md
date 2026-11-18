# Guía 13 — El recetario oficial de casos de uso

**Objetivo:** los patrones de uso probados de los propios docs de Cognition, organizados como un recetario — qué cortar para Devin, y más de 40 recetas documentadas con prompts para copiar.
**Nivel:** empieza aquí para amplitud
**Fuentes:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) · [use-case tutorials](https://docs.devin.ai/use-cases/index.md)

## La única regla detrás de todo

Orientación oficial, lógica literal: elige trabajo **wide & shallow** — un backlog grande de tareas simples y horizontalmente escalables vence a builds complejas desde cero, siempre.

| Tarea ideal | Anti-tarea |
| --- | --- |
| Subtareas repetitivas a complejidad de ingeniero júnior | Features complejas net-new |
| < 90 minutos de trabajo manual por porción | Cualquier cosa que no se puede dividir |
| Verificación pasa/falla objetiva | "Me parece bien" |
| Aislada, retrocompatible, paralelizable | Dependencias enredadas |

Cuatro grandes formas de porción de los docs: **migraciones, refactors, modernizaciones, backlogs de tech debt.**

## El catálogo de recetas

Todo lo de abajo es un caso de uso documentado en la galería oficial — cada una viene con un prompt listo para copiar. Organizado por el trabajo que le quita a un humano de su semana.

### Incidentes & salud de producción

| Receta | Mecanismo |
| --- | --- |
| Auto-investigar alertas Datadog/PagerDuty | Disparo webhook/API → la sesión investiga en el incendio |
| Auto-generar postmortems | PagerDuty resolve → Devin redacta timeline, causa raíz, action items |
| Correcciones diarias de errores de Sentry | Cron nocturno trae errores nuevos → PRs de corrección por la mañana |
| Depurar un bug report de punta a punta | Entrégale el informe + logs de Datadog + acceso al DB → causa raíz |

### Higiene programada (la página de mayor ROI de los docs)

| Receta | Cadencia |
| --- | --- |
| PRs semanales de update de dependencias | Semanal: paquetes desactualizados → PRs de upgrade testeados |
| E2E nocturno en staging | Nocturno: corre la suite, abre tickets para fallos |
| Changelog semanal de PRs mergeados | Viernes: changelog categorizado → Slack |
| Digest diario de salud Datadog | Diario: escaneo de errores → digest en Slack |
| Auditoría diaria del design system | Diario: señala colores hardcodeados/tokens faltantes en PRs mergeados |
| Limpieza de feature flags | Una sesión única quita flag + código muerto post-release |
| Digest semanal de estado en Notion | Semanal: resumen de PR/commit → Notion |
| PRs desde transcripciones de reuniones | Cada hora: poll Granola → extrae tareas de eng → sesiones hijas |

### Calidad de código

| Receta | Mecanismo |
| --- | --- |
| Auto-corregir bugs de PR antes del merge | Devin revisa cada PR, empuja correcciones a la rama |
| Añadir tests unitarios a un servicio | Construye un skill de escritura de tests, aplícalo a charge flows/refunds/webhooks |
| Cazar regresiones visuales | Skill de repo: screenshot de cada página afectada antes del PR |
| Checklist de migración en cada PR | Skill de repo caza ops destructivas, valida cambios de schema |
| Dividir un router monolítico | Router Express de 2.000 líneas → rutas de dominio con middleware compartido |
| Subir cobertura de código | Devin analiza la suite, escribe tests para cubrir las brechas |
| Parchear CVEs conocidas entre repos | Skills oficiales ([devin-vuln-fixes](https://github.com/cognitionai/devin-vuln-fixes)): inventario solo-lectura → gate de aprobación → parche en objetivo confirmado → tests antes/después → un PR por repo |

### Migraciones & feature work

| Receta | Mecanismo |
| --- | --- |
| REST→GraphQL de 50 archivos | Alcance → paquetes sin conflicto → paralelo (Guía 11) |
| Skill de upgrade React 18→19 | Convierte la guía oficial de upgrade en un skill por fases para tu codebase |
| Spec OpenAPI → implementación | YAML spec → handlers Express + validación Zod + Supertest |
| Flujo de checkout Stripe | Spec → flujo funcional + tests + verificación en navegador |
| i18n en una app Next.js | install next-i18next, extracción de strings, chequeo en navegador en 3 idiomas |
| Figma → pixel-perfect | Figma MCP → componentes desde mockups |
| Dockerizar una app Django | Dockerfile multi-stage + compose para Django/Postgres/Redis |

### Gestión de proyecto & datos

| Receta | Mecanismo |
| --- | --- |
| Auto-triage de bugs vía Linear | Label aplicada → Devin investiga |
| PRDs → tickets de sprint | PRD en Notion → tickets Linear acotados |
| Planes de implementación de backlog | Multi-seleccionar tickets Linear → planes con score de confianza |
| Consultas `/dana` en Slack | Consultas de base de datos en lenguaje natural desde cualquier canal |
| Dashboard custom de uso de API | Devin construye un dashboard a medida sobre la API v3 |

### Mejorando al propio Devin ("Devin Optimization")

| Receta | Lección |
| --- | --- |
| Cortar un prompt de feature 42→12 ACUs | Autopsia de una sesión cara: 3 causas raíz → reescribir el prompt |
| Carrera de 3 sesiones en un problema | Sesiones paralelas prueban estrategias de optimización competidoras; la mejor gana |
| 8 sesiones paralelas de noche | 8 módulos sin tests → PRs de unit tests por la mañana |
| Evaluar 30 librerías | Una sesión por librería → comparación rankeada con score |
| Convertir un hotfix en skill | Extrae una sesión de incidente exitosa en un skill reutilizable |
| Dedup semanal de knowledge | Sesión programada mergea/limpia conflictos de sugerencias de knowledge |
| Guía de onboarding de equipo | Devin lee sus propios docs → una guía de primeros pasos para tu stack |

## Cómo usar este recetario

1. Elige una receta de **Higiene programada** — es la primera victoria más barata (un bucle nocturno/semanal sobre el que dejas de pensar)
2. Añade una de **Incidentes** si tienes PagerDuty/Datadog/Sentry
3. Cuando una receta funciona, congélala como un **skill** (Guía 12) o un **Bot** (Guías 1–5) — cada fila de arriba sobrevive como uno de los dos

## Checklist de verificación

- [ ] Una receta de higiene está corriendo en horario y produjo su primer PR/informe
- [ ] Su salida está congelada como skill, playbook o Bot — no viviendo en la cabeza de alguien

## Trampas

- **Diez recetas, cero congeladas.** Una receta que sigue siendo un prompt manual queda olvidada el viernes — operacionaliza o descarta.
- **Prompts copiados sin la verificación de tu repo.** Los prompts de la galería asumen que existe una suite de tests; adapta la *comprobación*, no solo la tarea.

## Prueba de conocimiento

1. ¿Por qué empezar con una receta de higiene programada en vez de respuesta a incidentes? *(La victoria más barata posible — corre mientras duermes, y una corrección de lint nocturna errada es recuperable; una acción de incidente errada no.)*
2. ¿Qué previene realmente "congelar una receta como skill o Bot"? *(Deriva de prompt y dependencia de persona única — la receta sobrevive a quien la escribió.)*
3. ¿Por qué adaptar la parte de verificación de un prompt de la galería antes que la parte de la tarea? *(La tarea describe intención; la comprobación es lo que tu repo puede probar — comprobaciones erradas producen basura confiada.)*

## Fuentes

- [Use-case gallery](https://docs.devin.ai/use-cases/gallery/index.md) — todas las recetas de arriba, cada una con prompts listos
- [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) — la doctrina de corte
- [Use-case tutorials](https://docs.devin.ai/use-cases/index.md) — integración de API, cobertura de código, containerización, componentes frontend, MCP
- Relacionado: [Guía 11 — Migraciones a escala](migrations-at-scale.md) · [Guía 6 — Automatizaciones](automations-101-event-driven.md)
