# Guía 11 — Migraciones a escala

**Objetivo:** ejecutar una migración grande (lenguaje, framework, base de datos, dependencia, arquitectura) como cientos de PRs pequeños verificados en vez de una reescritura heroica.
**Nivel:** intermedio → avanzado
**Fuentes:** [Best Practices](https://docs.devin.ai/use-cases/best-practices.md) · [Migration & Modernization](https://docs.devin.ai/use-cases/migration-modernization.md) · ejemplos de migración: [Java upgrades](https://docs.devin.ai/use-cases/examples/java-upgrades.md), [COBOL](https://docs.devin.ai/use-cases/examples/cobol-modernization.md), [SAS→PySpark](https://docs.devin.ai/use-cases/examples/sas-to-pyspark.md), [JS→TS](https://docs.devin.ai/use-cases/examples/javascript-to-typescript.md), [NoSQL→SQL](https://docs.devin.ai/use-cases/examples/nosql-to-sql.md) · caso Nubank

## El playbook oficial

Los docs del propio Devin son directos sobre lo que escala: **wide & shallow** vence a **tall & deep**. Una migración es el trabajo wide-and-shallow canónico — la misma pequeña transformación aplicada a cientos de unidades independientes.

```text
migración ──► cortar en unidades aisladas (<90 min cada)
                     │
            ┌────────┴────────┐
            ▼                 ▼
       skill para la     sesiones paralelas,
       transformación    una porción cada una
            │                 │
            └────► verificar por porción (tests/build/CI)
                             │
                  revisión humana → merge → repetir
```

## Paso 1 — Comprueba que tu migración califica

De los criterios oficiales — la mayoría debe cumplirse:

- Alto volumen de subtareas repetitivas
- Complejidad de ingeniero júnior por porción
- Cambios aislados, incrementales, retrocompatibles
- **Verificación objetiva por porción** (el requisito duro: tests, build, CI o un script propio)
- Dependencias mínimas entre porciones

No califica: una reescritura de repo entero donde todo debe aterrizar a la vez.

## Paso 2 — Corta

La porción es la unidad atómica más pequeña — un archivo, un notebook, un módulo:

| Regla | Por qué |
| --- | --- |
| < 90 minutos de ingeniería manual por porción | La fiabilidad de Devin es por porción |
| Independiente + retrocompatible | Las porciones corren en paralelo y mergean en cualquier orden |
| Cada porción lleva su propia verificación | Sin verificación, sin automatización — este es el gate de fallo |

Ejemplo (oficial): una migración REST→GraphQL de 50 archivos → acotarla, dividir en paquetes de trabajo sin conflictos, correr en paralelo.

## Paso 3 — Escribe la transformación como un skill

Un skill = la receta repetible que toda sesión ejecuta. Ejemplo oficial (Java 7→8, abreviado):

```text
## Procedure
1. Verify the project is on Java 7
2. Install the Java 8 JDK
3. Update build configuration
4. Identify and replace deprecated Java 7 APIs
5. Analyze for Java 8 enhancement opportunities
6. Update unit tests
7. Test thoroughly
8. Update documentation
9. Build and verify
```

Escribe el tuyo con: pasos explícitos, una referencia de punta a punta (una guía o vídeo) y **múltiples ejemplos de código antes/después** — los pares entrada/salida son la señal de mayor calidad que puedes dar.

## Paso 4 — Ejecuta sesiones paralelas

Con el skill fijado, distribuye porciones entre sesiones — la [API](https://docs.devin.ai) o las sesiones hijas de un Bot (Guía 4). Cada porción → una sesión → un PR. La revisión humana hace el gate del merge a `main`.

A escala los números se componen: la migración ETL de millones de líneas de Nubank corrió este bucle hasta 8–12× de eficiencia — y un Devin fine-tuned bajó el tiempo por tarea de ~40 → ~10 minutos.

## Paso 5 — Vigila la tasa de error, no la barra de progreso

Las tasas de error pequeñas se componen a través de miles de porciones. Opera en un dashboard, no en sensaciones:

- Sigue la tasa de éxito de porción al primer intento — el skill es tu punto de corrección, no las sesiones
- Las porciones fallidas alimentan de vuelta el skill (el bucle de los propios docs: *"feed session links into Devin to patch the gaps"*)
- El orden de merge es libre porque las porciones están aisladas — explótalo

## Checklist de verificación

- [ ] Toda porción termina en ~90 min y mergea independientemente
- [ ] Una porción que falla la verificación produce una corrección o un ticket señalado — nunca un merge silencioso
- [ ] El skill mejoró mediblemente en las primeras 20 porciones (menos correcciones humanas por porción)
- [ ] El progreso es contable: N/M porciones migradas, tasa de éxito visible

## Trampas

- **Migraciones sin cortar.** "Migra el repo entero" es el antipatrón oficial — sin aislamiento, sin paralelismo, sin verificación por unidad.
- **Sin ejemplos antes/después.** El skill sin ejemplos produce un estilo distinto por sesión.
- **Saltarse la revisión humana.** Paralelo ≠ desatendido — cada porción sigue siendo revisada antes de `main`.

## Prueba de conocimiento

1. ¿Por qué porciones "wide and shallow" en vez de "deep and complete"? *(Cada porción debe aterrizar en verde — un PR verificado de 90 minutos se compone; un mega-branch de 3 días se pudre contra main.)*
2. ¿Por qué cada porción necesita su propia verificación? *(Sin prueba por porción, una migración de 500 PRs son 500 diffs no verificados — la superficie de fallo multiplica en vez de dividir.)*
3. Nubank reportó 8–12× de eficiencia — ¿qué hizo esa cifra creíble y no marketing? *(Metodología publicada: tiempos de etapa medidos antes/después en pipelines ETL reales, no una proyección.)*

## Fuentes

- [Best Practices — docs.devin.ai](https://docs.devin.ai/use-cases/best-practices.md)
- [Migration & Modernization + 5 playbooks de ejemplo](https://docs.devin.ai/use-cases/migration-modernization.md)
- [Use-case gallery — Migrations](https://docs.devin.ai/use-cases/gallery/index.md)
- Relacionado: [Guía 7 — Rollout enterprise](enterprise-playbook.md) (la Forma 1 es esta guía a escala de org)
