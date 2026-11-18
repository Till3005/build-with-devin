# Guía 5 — Enjambre anclado en referencia

**Objetivo:** dirigir un enjambre de agentes para escribir un sistema grande y *verificable* — donde la corrección se comprueba continuamente contra una referencia confiable, no contra sensaciones.
**Nivel:** avanzado
**Implantación de origen:** el **"Phil"** de Harvey — ~30 agentes escribieron un motor de editor colaborativo compatible con Word en Rust + TypeScript: **más de 1M de líneas en 3 semanas, cero ingenieros humanos**. Verificado continuamente contra el comportamiento real de Microsoft Word y negociaciones de abogados simuladas. Los humanos dirigieron mediante memoria + logs de decisión, nunca leyendo código.
**Fuentes:** relato de lanzamiento de Gabe Pereyra ([vía @gabepereyra](https://x.com/gabepereyra)) · [post de lanzamiento](https://devin.ai/blog/introducing-devin-bots)

## El patrón

Un enjambre falla cuando nadie puede decir si la salida es correcta. Phil funcionó porque cada línea podía comprobarse contra una **referencia de verdad**: el Microsoft Word real. El trabajo del equipo de agentes era *igualar* — un objetivo objetivo y continuamente verificable — no *inventar*.

```text
   sistema de referencia (verdad)
            ▲ compara
            │
┌───────────┴────────────┐
│  enjambre de ~30 agentes│──► 1M+ LOC (Rust + TypeScript)
└────────────────────────┘
            ▲ dirige
            │
   humanos: memoria + logs de decisión
   (nunca leyendo el código)
```

## Cuándo usarlo

| Buen ajuste | Mal ajuste |
| --- | --- |
| Reimplementar una spec (formato de archivo, protocolo, editor, compilador) | Productos greenfield sin respuesta objetiva |
| Portado/migración con oráculo (el sistema legado sigue corriendo) | UX nueva donde "correcto" es una llamada de juicio |
| Cualquier cosa difeable contra un sistema funcionando | Sistemas donde la corrección necesita usuarios |

La prueba de fuego: **¿puede una máquina decidir "correcto" sin ti?** Si sí, un enjambre escala; si no, usa un Bot product-owner (Guía 2).

## Paso 1 — Asegura la referencia primero

Antes de que cualquier agente escriba código, la comprobación debe existir:

- La referencia de Harvey: **comportamiento real de Microsoft Word** — los documentos renderizados en el editor del enjambre tenían que igualar a Word
- La tuya puede ser: el sistema legado aún corriendo, una suite de conformidad, golden files, un corpus de tests de la spec, un contrato de API

Pon la comparación en CI o en un script que el enjambre ejecute constantemente — "¿la salida coincide con la referencia?" debe ser barato y automático, o los agentes se desvían entre comprobaciones.

## Paso 2 — Descompón en porciones con dueño

~30 agentes no compartían un backlog — el trabajo se cortó para que cada agente fuera dueño de un subsistema (modelo de documento, motor de layout, protocolo de colaboración, …). Estrúcturalo como el organigrama de la Guía 4, salvo que cada "empleado" es una sesión de código apuntando a una frontera de módulo:

```text
You own the <module>. Its contract is <interface/reference behavior>.
Your PRs are accepted when the reference checks pass — not when the
code looks done.
```

## Paso 3 — Los humanos dirigen por encima del código

Nadie en Harvey leyó el millón de líneas. La dirección ocurrió mediante:

- **Memoria** — los hechos acumulados del Bot sobre decisiones tomadas y por qué
- **Logs de decisión** — lo que el enjambre eligió en cada bifurcación
- **Mensajes de dirección** — "prioriza la fidelidad de track-changes sobre el rendimiento esta semana"

Tu superficie de revisión es el *rastro de decisiones*, no el diff. Si te descubres leyendo código generado para saber qué pasa, pide al orquestador el log de decisiones.

## Paso 4 — Validación adversarial encima

Harvey añadió una segunda capa: **negociaciones de abogados simuladas** — uso realista que aflora lo que una suite de conformidad pierde. Tu equivalente: una capa de escenarios sobre el diff de referencia — workflows reales, inputs adversariales, fuzzing. Las comprobaciones de referencia atrapan lo *incorrecto*; las de escenario atrapan lo *frágil*.

## Checklist de verificación

- [ ] Existe una comprobación de referencia automatizada que corre contra cada cambio
- [ ] El criterio de aceptación de cada agente es "la referencia pasa", nunca "código escrito"
- [ ] Puedes responder "qué decidió el enjambre y por qué" desde logs/memoria sin leer código
- [ ] Un módulo roto deliberadamente es atrapado por la comprobación de referencia, no por ti

## Trampas

- **Escalar antes del oráculo.** Un enjambre sin comprobación solo produce volumen — Phil funcionó porque Word siempre fue el juez.
- **Revisar diffs.** No escala más allá de ~2 agentes; te conviertes en el cuello de botella y pierdes la ventaja de velocidad del enjambre.
- **Propiedad ambigua.** Dos agentes editando un módulo producen infierno de merge — las fronteras de propiedad son la arquitectura.

## Prueba de conocimiento

1. ¿Por qué funcionó el enjambre de Harvey donde la mayoría de los intentos multi-agente colapsan? *(Una referencia externa confiable — el comportamiento real de Word — hizo la corrección comprobable por máquina a velocidad de enjambre.)*
2. ¿Por qué los humanos dirigieron mediante memoria y logs de decisión en vez de revisar código? *(1M+ LOC en 3 semanas excede cualquier capacidad humana de lectura; la dirección ocurre en la capa de intención.)*
3. ¿Qué prerequisito comprobarías antes de intentar este patrón? *(Si tu dominio tiene una referencia contra la que el enjambre pueda comprobarse — si no, construye primero el oráculo.)*

## Fuentes

- [@gabepereyra](https://x.com/gabepereyra) — relato del Phil de Harvey: ~30 agentes, 1M+ LOC, verificación por referencia a Word, simulaciones de abogados
- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots)
- Relacionado: [Guía 4 — Organización multi-Bot](bots-203-multi-bot-org.md) (misma jerarquía, propósito distinto: operación vs. construcción)
