# Guía 1 — Tu primer Bot

**Objetivo:** crear un Devin Bot que se haga dueño de un resultado, y aprender las seis mecánicas sobre las que se construyen todos los guías siguientes.
**Nivel:** empieza aquí · **Tiempo:** ~15 minutos
**Fuente:** [documentación oficial de Bots](https://docs.devin.ai/work-with-devin/bots), [post de lanzamiento](https://devin.ai/blog/introducing-devin-bots)

## Qué es un Bot

Una sesión atiende una petición. Un Bot *es dueño de un resultado*: declaras la meta una vez en su chat, él planifica el trabajo, inicia una sesión Devin hija para cada pieza, las monitoriza y solo te trae lo que requiere tu juicio. Persiste — memoria, sesiones y automatizaciones sobreviven durante semanas.

Las seis mecánicas, en el orden en que las encontrarás:

| Mecánica | Qué es | Dónde la tocas |
| --- | --- | --- |
| Chat | Un hilo para todo lo que el Bot posee — metas, informes, preguntas | La página del Bot / Slack / iMessage |
| Sessions | Cada pieza de trabajo corre como su propia sesión Devin en su propia máquina | Creadas y monitorizadas por el Bot |
| Needs you | Decisiones, revisiones de PR, solicitudes de permiso, informes — una sola lista | Arriba en el chat del Bot |
| Memory | Lo que el Bot aprende, guardado como archivos, leído al inicio de cada sesión | Settings → Memory |
| Instructions | Reglas permanentes escritas por personas, leídas al inicio de cada sesión | Settings → General |
| Access | Las conexiones/secretos del propio Bot, más grants entre Bots | Settings → Access |

## Paso 1 — Crearlo

Sidebar → **Bots** → *Create new Bot* → elige una plantilla o *Start from scratch* → ponle nombre.

Un Bot nuevo es privado para ti hasta que lo compartas. Su uso cuenta en tu plan como cualquier sesión.

> Consejo: una plantilla trae instrucciones para una función (QA Engineer, Data Analyst, …). *Start from scratch* es la elección correcta para las guías de este repositorio — escribirás el prompt de resultado tú mismo.

## Paso 2 — Asignar el resultado

El primer mensaje es el input más importante que un Bot recibirá jamás. Dale una *meta*, no una tarea:

```text
You own the Android app now. Keep it at feature parity with iOS.
```

Ese es el prompt literal con el que empezó el Android Bot de Cognition. Compara:

| Débil (una tarea) | Fuerte (un resultado) |
| --- | --- |
| "Fix the checkout button" | "You own checkout. Keep it fast, correct, and covered by tests." |
| "Update the docs" | "You own the docs. Keep them in step with `main`." |
| "Watch CI" | "You own build health on `main`. When a check regresses, find the cause and fix it." |

Una tarea termina cuando está hecha; un resultado hace que el Bot replanifique para siempre.

## Paso 3 — Trabajar con él

Una vez definido el resultado, la mayoría de tus mensajes son check-ins:

```text
anything waiting on me?
```

Abre **Needs you** (arriba del chat) cuando el Bot marque algo:

| Elemento | Tu jugada |
| --- | --- |
| Decision | Elige una opción — el Bot marca su recomendación |
| Review PR / Merge PR | Revisar o mergear |
| Permission request | Aprobar o rechazar nuevo acceso, una automatización, un host de red o un aumento del límite de uso |
| Report / FYI | Léelo |

Puedes responder con tus propias palabras, posponer o descartar cualquier elemento.

## Paso 4 — Dirigir por la memoria, no por microgestión

- **Instructions** (Settings → General): tus reglas permanentes — leídas al inicio de cada sesión que el Bot ejecuta. Pon aquí la política duradera, no en el chat.
- **Memory** (Settings → Memory): archivos que el propio Bot escribe — preferencias, correcciones, datos del proyecto. Para cambiar lo que recuerda, díselo en el chat ("remember: we deploy via Cloud Run, never bare VMs"). Todo el que pueda usar el Bot puede leer su memoria — trata la memoria de un Bot compartido como compartida.

El patrón que escala: corrige el Bot una vez, deja que escriba la corrección en memoria, y cada sesión futura la hereda. Cognition mergea más de 2.000 PRs/semana con este bucle.

## Paso 5 — Ponerlo donde trabajas

- **Slack:** dale al Bot su propia app de Slack para que tu equipo pueda @-mencionarlo o mandarle DM (Settings → Slack). Toda implantación de equipo reportada funciona así — el Bot se convierte en un compañero nombrado en un canal.
- **iMessage:** escribe al Bot desde tu móvil.
- **Web:** la sección Bots de la sidebar lista los tuyos y los compartidos contigo.

## Paso 6 — Programaciones y modos

- **Automations:** pídelo en el chat — *"run a summary of open PRs every weekday morning"* — y el Bot propone la automatización para tu aprobación única. Gestiónalas en Settings → Automations (pausar/reanudar/eliminar).
- **Modes:** el Bot tiene su propio modo más un valor por defecto de **Child Capability** para las sesiones que crea (p. ej. `Normal / Ultra` en el selector de modo del chat). También puedes pedir un modo distinto en cualquier sesión concreta.

## Ciclo de vida

| Acción | Efecto |
| --- | --- |
| Recycle | Termina la sesión actual; una nueva empieza en la próxima apertura. En el menú del chat. |
| Archive | Detiene las respuestas, lo quita de las listas de Bots, elimina su app de Slack y los grants entre Bots (desarchivar no los restaura — los configuras de nuevo). |
| Delete | Permanente: configuración, sesiones, memoria, automatizaciones. No se puede deshacer. |

Solo el creador y los roles con Manage Bots ven Archive/Delete. En planes Enterprise, `Use Bots` / `Manage Bots` / `Manage Bots across the enterprise` son permisos separados en roles personalizados.

## Checklist de verificación

- [ ] Bot creado y nombrado; prompt de resultado enviado en el chat
- [ ] El Bot inició al menos una sesión hija sin que se lo pidieran dos veces
- [ ] Una decisión/PR/solicitud de permiso apareció en **Needs you** y la resolviste
- [ ] Una corrección que diste en el chat aparece como archivo de memoria en Settings → Memory
- [ ] (Opcional) Bot alcanzable por @-mención en Slack

## Trampas

- **Prompts con forma de tarea.** "Fix X" produce una sesión, no un Bot. Si el Bot termina y se queda callado, el prompt era una tarea — reformúlalo como propiedad de un resultado.
- **Chat para política.** Las reglas escritas en el chat desaparecen con el scroll; las reglas en Instructions se leen en cada sesión. Chat = dirección y respuestas; Instructions = ley.
- **Ignorar Needs you.** Los Bots están diseñados para agrupar las llamadas de juicio — revisa una o dos veces al día, no continuamente.

## Prueba de conocimiento

1. ¿Qué sobrevive entre las sesiones de un Bot que una sesión aislada no tiene? *(La memoria — más el resultado permanente, las programaciones y las superficies.)*
2. ¿Por qué un Bot usa "needs-you" en lugar de preguntar a mitad de sesión? *(El juicio va a un hilo asíncrono; el humano no es una llamada bloqueante en el bucle.)*
3. ¿Qué mecánica convierte "una sesión lista" en "un empleado"? *(La propiedad de un resultado — la meta persiste después de que cualquier sesión termina.)*

## Fuentes

- [Devin Bots — docs](https://docs.devin.ai/work-with-devin/bots)
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Siguiente: [Guía 2 — Bot product-owner](bots-201-product-owner.md)
