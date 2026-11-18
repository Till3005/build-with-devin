# Guía 6 — Automatizaciones orientadas a eventos

**Objetivo:** conectar eventos externos — Slack, Teams, GitHub, Linear, Jira, PagerDuty, cron, webhooks — a sesiones Devin que se inician solas.
**Nivel:** empieza aquí (guía de plataforma) · **Tiempo:** ~20 minutos
**Fuente:** [docs de Automations](https://docs.devin.ai/product-guides/automations) · [walkthrough oficial en vídeo](https://www.youtube.com/watch?v=6xxKtIpgOyE)

## La anatomía

Toda automatización tiene cuatro partes:

| Parte | Qué hace |
| --- | --- |
| Trigger | El evento que la dispara — un mensaje de Slack, un CI que falla, un tick de cron, un webhook HTTP |
| Conditions | Filtros opcionales — solo la label `bug`, solo este repo, solo mensajes que contienen `/devin` |
| Preflight check | Filtro LLM o script opcional que corre *después* del match, antes de las acciones — puede saltar el evento o dividirlo en ítems de trabajo |
| Action | Lo que corre: iniciar una sesión, mandar mensaje a una sesión existente, monitor de triaje o notificación por email |

## Catálogo de triggers

| Fuente | Dispara en | Uso canónico |
| --- | --- | --- |
| Slack | Nuevo mensaje, reacción añadida, mención a user-group | Triaje de `#incidents`; reacción 🚨 → investigar |
| Microsoft Teams | Mensaje, reacción | Responder a bug reports en el hilo donde se postearon |
| GitHub | Issue, comentario en issue, PR, review de PR, check run, push | Auto-arreglar CI fallando; comentario `/devin` → sesión |
| GitLab | MR, comentario en MR, issue, push, pipeline | Arreglar pipelines que fallan |
| Linear | Issue creada/etiquetada/status/prioridad/asignada/movida | Implementar tickets cuando se asignan a Devin |
| Jira | Issue creada/actualizada/etiquetada/status/asignada/comentada | Lo mismo, en formato Jira |
| Pylon | Issue creada/etiquetada/status | Triaje de bugs de clientes |
| PagerDuty | Incidente disparado/reconocido/resuelto | Investigar incidentes de alta urgencia al momento |
| Schedule | Cron o único | Barrido diario de Sentry, updates semanales de deps, smoke tests nocturnos |
| Webhook | Cualquier POST HTTP | Todo lo demás — Datadog, Sentry, tus propios sistemas |

Múltiples triggers en una automatización actúan como O — p. ej. disparar *o* en un CI fallando de GitHub *o* en una reacción de Slack.

## Receta 1 — `/devin` en cualquier issue

El trigger más implantado en el mundo:

```text
Trigger:   GitHub → issue comment, repo = your/repo
Condition: comment body starts with "/devin"
Action:    Start session — prompt includes the event payload
```

Resultado: cualquiera del equipo comenta `/devin investigate this` en una issue, y una sesión lo toma con todo el hilo como contexto.

## Receta 2 — Autorreparación de fallo de CI

```text
Trigger:   GitHub → check run, repo = your/repo
Condition: conclusion = failure
Action:    Start session: "CI check <name> failed on this commit.
            Diagnose the failure from the logs, fix it, and push to
            the same branch."
```

El payload del evento lleva el check que falló + commit a la sesión — sin copiar y pegar.

## Receta 3 — Barrido programado

```text
Trigger:   Schedule → daily 09:00
Action:    Start session: "Sweep yesterday's Sentry issues in
            <project>. File the top 3 by impact as tickets and
            start the most actionable one."
```

Los bucles de higiene diarios (barridos de Sentry, actualizaciones de dependencias, smoke tests) son las automatizaciones de mayor ROI — convierten "alguien debería revisar" en "está revisado".

## Tipos de acción, cómo elegir

| Acción | Usa cuando |
| --- | --- |
| Start session | El default — cada evento recibe una máquina y contexto nuevos |
| Message session | Una sesión de larga vida mantiene estado — aliméntala de eventos (la semilla de un Bot) |
| Triage Devin | Un Devin persistente vigila un canal entero de Slack y genera investigaciones hijas (ver Devin Oncall para incidentes) |
| Email notification | Solo avisarte de que corrió |

**Automatización vs. Bot:** las automatizaciones son tuberías tontas — evento entra, sesión sale. Un Bot añade memoria, juicio y planificación multi-sesión alrededor de los mismos triggers. Empieza con automatizaciones; gradúa a un Bot cuando el trabajo necesite continuidad (Guías 2–5).

## Construirla

Tres caminos de creación en la página de Automations:

1. **Create** — el editor en blanco: elige trigger → conditions → action
2. **Template** — la galería de automatizaciones preconfiguradas para workflows comunes
3. **Generate with Devin** — descríbela en inglés (*"when a CI check fails on my-org/my-repo, have Devin fix it and push to the same branch"*), revisa la config generada

Notas que muerden a la gente:

- Los triggers de Slack necesitan Devin invitado al canal **y** tu Slack personal conectado en Settings → Connections
- Los canales privados de Teams solo disparan con @mención
- Un trigger de GitHub debe nombrar un repo específico
- Gestiona automatizaciones declarativamente con el **provider Terraform** si ejecutas muchas

## Checklist de verificación

- [ ] Dispara el trigger manualmente una vez (comenta `/devin test`, o haz push de un commit que falla) y observa una sesión iniciar con el payload del evento
- [ ] Un evento que no casa (label incorrecta, canal incorrecto) no hace nada
- [ ] La salida de la acción cae donde esperabas (PR, hilo de Slack, ticket)

## Trampas

- **Bucles.** Una automatización cuya salida puede redispararse a sí misma (Devin comenta en un PR, el trigger vigila "nuevo comentario") quemará sesiones para siempre. Filtra por autor, label o subtipo de evento.
- **Tormentas de trigger.** Un webhook que dispara por commit en vez de por PR puede crear 50 sesiones en un día movido. Controla: una automatización por *unidad reclamable* de trabajo, no por evento crudo.
- **Sin gate de aprobación.** Auto-mergear o auto-desplegar en un trigger salta el punto de control humano — mantén el patrón "la sesión abre un PR, una persona mergea" a menos que tengas una razón medida para no hacerlo.

## Prueba de conocimiento

1. Un compañero quiere que Devin "vigile cada notificación de GitHub" — ¿qué le pides que estreche primero? *(Qué subtipo de evento realmente implica trabajo accionable — una label aplicada, una review solicitada — no toda notificación.)*
2. ¿Por qué un evento que no casa debe producir *ninguna* sesión en vez de una sesión que decide hacer no-op? *(Las sesiones cuestan ACUs; filtrar upstream es gratis, filtrar dentro de una sesión no.)*
3. ¿Cuándo una automatización necesita un Bot? *(Cuando el trabajo disparado necesita juicio acumulado en el tiempo — memoria, prioridades, un resultado permanente.)*

## Fuentes

- [Automations — docs](https://docs.devin.ai/product-guides/automations)
- [Devin Automations QuickStart (vídeo)](https://www.youtube.com/watch?v=6xxKtIpgOyE)
- Relacionado: [Guía 3 — Bot centinela programado](bots-202-scheduled-sentinel.md) para añadir juicio de Bot sobre un cron
