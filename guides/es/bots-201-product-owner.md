# Guía 2 — Bot product-owner

**Objetivo:** un Bot que gestiona como producto una superficie completa — abre sus propios tickets, los construye, mergea e informa a diario.
**Nivel:** intermedio · **Carga humana tras el setup:** ~1 mensaje por cada 6 PRs mergeados
**Implantación de origen:** el **Android Bot** de Cognition — envió la app Android de Devin a la beta abierta de Google Play en **44 días**: 1.134 PRs mergeados, 344.651 líneas de Kotlin, 2.841 tests de screenshot, 1.217 tickets. Su humano envió **183 mensajes en total** (22 días de silencio) y **el 88% de los PRs se auto-mergearon**. Ahora es dueño de la paridad de features Android/iOS.
**Fuentes:** [post de lanzamiento](https://devin.ai/blog/introducing-devin-bots) · [Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) · notas de dogfooding de Russell Kaplan

## El patrón

Un Bot es dueño de una *superficie* — una app, un sitio, un servicio — como un PM la poseería: decide qué construir, lo convierte en tickets, ejecuta una sesión por ticket y mantiene la superficie viva indefinidamente. El humano actúa como el ejecutivo al que reporta.

```text
Bot ──► abre tickets ──► sesión por ticket ──► PR ──► CI + Devin Review ──► merge
 │                                                                            │
 └──────────── informe diario + decisiones Needs-you ◄───────────────────────┘
```

## Prerequisitos

- Un repositorio que el Bot pueda poseer por completo (repo de app con CI, review y ruta de merge)
- Devin Review habilitado en el repo, y checks de CI conectados
- Una app de Slack para el Bot (recomendado — toda implantación documentada reporta en Slack)

## Paso 1 — El prompt de resultado

El real, literal de Cognition:

```text
your job is to product manage the android app. Basically, you're going to
autonomously create the entire thing, but we need to figure out what the
blockers are for you doing that first.
```

Plantilla reconstruida para tu superficie:

```text
Your job is to product manage <surface>. You're going to autonomously
<build / keep parity with <reference>>, but first enumerate the blockers
to you doing that — where the code lives, how to build and test it, and
how changes merge — then start working through them.
```

Fíjate en la forma: **propiedad + autonomía + bloqueadores primero**. No le entregues un backlog; entrégale un mandato y haz que aflore lo que necesita.

## Paso 2 — Fase uno: desbloquear, no construir

El Android Bot no escribió código primero — enumeró bloqueadores: acceso al repo, comandos de build, cómo probar en dispositivo/emulador, la ruta de merge. Tu versión de esa lista:

- ¿Puede compilar el proyecto en su máquina? (Dependencias de blueprint/snapshot)
- ¿Puede producir artefactos instalables (APK/TestFlight/deploy de preview)?
- ¿Conoce la política de merge — qué checks deben pasar, quién revisa?
- ¿Tiene las credenciales que necesita (claves de tienda, firma) — o una solicitud de grant documentada para ellas?

Déjalo terminar esta auditoría antes de que abra tickets de producto. Cada bloqueador que resuelve aquí es una sesión atascada que no verás después.

## Paso 3 — El bucle de trabajo

Una vez desbloqueado, el estado estacionario es:

1. El Bot abre un ticket para la siguiente unidad de trabajo que decida
2. Una sesión hija lo implementa y abre un PR — pequeño, con prueba de que funciona
3. CI + Devin Review hacen el gate del merge
4. El Bot mergea (o te pregunta cuando hace falta juicio — cae en Needs you)
5. El informe diario llega a Slack — los informes del Android Bot incluyen una **grabación de pantalla** de lo que cambió

Configura el reporting en las Instructions del Bot, no en el chat:

```text
Every day, post a report in #<channel>: what shipped, what's in flight,
what needs a human. Include a screen recording of visible changes.
```

## Paso 4 — Tu papel como ejecutivo

Los 183 mensajes en 44 días cayeron en dos cubos:

- **Llamadas de juicio** — aprobación de revisión de seguridad, un trade-off de diseño, una tarjeta de aprobación
- **Dirección** — "be more ambitious" es el ejemplo documentado

Todo lo demás — tickets, implementación, correcciones, auto-merges — es trabajo del Bot. Si estás respondiendo preguntas de implementación, estás gestionando demasiado bajo. Corrige una vez → cae en memoria → la siguiente sesión lo hereda.

## Estado estacionario

Tras el build inicial, el mismo Bot pasa a *poseer* la superficie:

- Mantiene paridad con un proyecto de referencia (el Android Bot ahora sigue las features de iOS)
- Triage de reports entrantes (atiende el feedback de la beta de Google Play)
- Captura regresiones entre superficies — el Android Bot encontró y arregló autónomamente una rotura en iOS/web causada por el cambio de otra persona

## Checklist de verificación

- [ ] La primera acción del Bot fue una auditoría de bloqueadores, no un PR
- [ ] Abre y trabaja su propia cola de tickets sin que se lo pidan
- [ ] Los PRs son pequeños y llevan prueba (tests, screenshots, grabaciones)
- [ ] El informe diario se publica en Slack con evidencia visible
- [ ] Pasaste un día entero enviando cero mensajes y los PRs siguieron mergeándose

## Trampas

- **Saltarse la fase de bloqueadores.** Un Bot product-owner que empieza a codar antes de poder compilar/probar/mergear produce PRs huérfanos.
- **PRs grandes.** La seguridad de la implantación viene de unidades pequeñas y verificables. Si los PRs engordan, instruye: *"one ticket, one concern, one PR."*
- **Revisar código en vez de dirección.** A más de 30 PRs/semana no puedes revisar cada diff — haz gate con CI + Devin Review + la evidencia del Bot, y gasta tus mensajes en dirección.

## Prueba de conocimiento

1. El Android Bot mergeó el 88% de sus propios PRs — ¿qué hizo el auto-merge lo bastante seguro? *(Existía verificación: 2.841 tests de screenshot más gates de review; la propiedad funcionó porque "hecho" era comprobable por máquina.)*
2. ¿Por qué abrir tickets en vez de lanzar sesiones directamente? *(Los tickets crean una cola auditable que el Bot tria por prioridad — y el humano revisa una cola, no 50 sesiones.)*
3. ¿Qué te dicen "22 días de silencio" sobre el modelo de control? *(La escalada-por-excepción solo funciona cuando la definición de hecho del Bot es verificable; el silencio es la feature, no descuido.)*

## Fuentes

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) — números y prompt del Android Bot
- [Exclusivo de Fortune](https://fortune.com/2026/11/17/exclusive-cognition-bets-on-devin-bots-coding-agents-in-challenge-to-anthropics-duet-and-openais-dots/) — 183 mensajes, 88% auto-merge, notas de dogfooding
- Relacionado: [Guía 4 — Organización multi-Bot](bots-203-multi-bot-org.md) cuando una superficie se convierte en negocio
