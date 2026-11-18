# Guía 9 — Playbooks & knowledge: codificando las convenciones de tu org

**Objetivo:** hacer que las sesiones y Bots de Devin sean fiables a escala de organización, escribiendo lo que tus mejores ingenieros dan por sentado — como playbooks (procedimientos repetibles) y knowledge (contexto permanente).
**Nivel:** intermedio · la capa que toda implantación grande publicada comparte
**Fuentes:** [docs.devin.ai](https://docs.devin.ai) · lecciones de implantación de la [Guía 7](enterprise-playbook.md)

## Por qué esta capa lo decide todo

Todo resultado enterprise publicado — el 8–12× de Nubank, el 92% de PRs de autoría de EBANX, los 1.600 seats de Wayfair — descansa sobre convenciones codificadas. Sin ellas, la salida de Devin varía por sesión: cada una redescubre tu stack, tus reglas de merge, tus hábitos de test. Con ellas, la sesión n.º 500 se comporta como tu mejor ingeniero en su mejor día.

Dos artefactos complementarios:

| Artefacto | Qué es | Analogía |
| --- | --- | --- |
| Knowledge | Contexto permanente que Devin lee — datos del repo, convenciones, trampas del entorno | Docs de onboarding |
| Playbook | Procedimiento nombrado y repetible — disparador, pasos, criterios de aceptación | Un runbook que cualquiera invoca |

## Paso 1 — Mina tus propias correcciones

El conocimiento más barato ya existe: recorre tus últimas 20 sesiones de Devin y recoge cada vez que escribiste una corrección — *"we deploy via Cloud Run,"* *"never `git push --force`,"* *"tests need `npm run db:seed` first."* Cada corrección es una entrada de knowledge con prueba de que importó.

Mina también:
- Comentarios de code review que los humanos repiten en los PRs de Devin
- Descripciones de PR que explican *por qué* un cambio se moldeó de cierta forma
- Docs de onboarding — todo lo que le dirías a un nuevo fichaje

## Paso 2 — Escribe entradas de knowledge que prenden

Las buenas entradas son una línea, imperativas y acotadas:

```text
- Deploy only via `make deploy-cloudrun` — never run gcloud directly.
- Migrations require a matching rollback file in prisma/rollbacks/.
- The staging seed user is qa+admin@corp.io; never create real-looking users.
```

Las malas entradas son ensayos, deseos ("write good tests") o secretos (nunca pongas credenciales en knowledge — usa el secrets store).

## Paso 3 — Playbooks para trabajo repetible

Un playbook empaqueta un procedimiento para que cualquier sesión (o Bot) lo ejecute igual. Estructura que funciona:

```markdown
# <Verbo + objeto> — p. ej. "Cut a release"
## When to use
<la condición disparadora>
## Steps
1. <paso determinístico>
2. ...
## Acceptance
<la comprobación pasa/falla>
## Failure modes
- <rotura conocida → qué hacer>
```

Publícalo a nivel org para que sesiones, automatizaciones y Bots puedan invocarlo — esto es lo que convierte una sesión exitosa aislada en capacidad de la organización.

## Paso 4 — Alimentando Bots

Las **Instructions** del Bot (Guía 1) son la versión acotada al Bot del knowledge — las reglas leídas al inicio de cada sesión. Pon la ley-del-puesto ahí; la ley-de-la-org en knowledge; los procedimientos en playbooks. El apilado mantiene cada artefacto pequeño y actualizado.

## Paso 5 — El bucle de corrección

El knowledge se pudre. El bucle que lo mantiene verdadero:

1. Una sesión/Bot se equivoca → lo corriges en el chat
2. El Bot escribe la corrección en memoria (o tú la añades a knowledge)
3. Revisión semanal: promociona ítems repetidos de la memoria del Bot al knowledge de la org; borra entradas que nadie disparó en un mes

Devin Coach (una plantilla oficial de Bot) existe exactamente para esto — reporta semanalmente dónde Devin se atascó y propone una corrección cada vez: una nota, un skill o un cambio de setup.

## Checklist de verificación

- [ ] Una sesión nueva en tu repo hace cero preguntas que tu knowledge ya responde
- [ ] La última corrección que diste a un Bot aparece en sus archivos de memoria
- [ ] Dos sesiones distintas ejecutan el mismo playbook y producen resultado de la misma forma

## Trampas

- **Escribir deseos.** "Follow best practices" no cambia nada; "run `npm run db:seed` before tests" lo cambia todo.
- **Set-and-forget.** El knowledge viejo es peor que ninguno — Devin lo sigue con confianza. Revisa mensualmente.
- **Duplicar docs.** El knowledge debe guardar lo que Devin *hace mal* o *no puede saber*, no una copia de tu wiki.

## Prueba de conocimiento

1. ¿Cuál es la diferencia entre un playbook y knowledge? *(Un playbook es un procedimiento repetible para una tarea nombrada; knowledge es contexto permanente que toda sesión debe asumir.)*
2. ¿Por qué "escribir lo que tus mejores ingenieros dan por sentado" es el cuello de botella enterprise real? *(La calidad del agente nunca fue el limitante — el contexto faltante lo es; la capa de knowledge es donde viven las convenciones de la org.)*
3. ¿Cuándo una convención se convierte en playbook vs. sigue siendo conocimiento tribal? *(La primera vez que una sesión se equivoca de una forma que un paso escrito habría prevenido.)*

## Fuentes

- [docs.devin.ai](https://docs.devin.ai) — knowledge, playbooks, instructions/memoria de Bot
- Relacionado: [Guía 7 — Patrones de rollout enterprise](enterprise-playbook.md) (esta capa es el paso que la mayoría de los rollouts se saltan)
