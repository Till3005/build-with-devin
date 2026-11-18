# Guía 10 — Devin Apps: herramientas en vivo desde un chat

**Objetivo:** describir una herramienta interna, dashboard o copia de staging — Devin la construye y la sirve en una URL estable que tu equipo abre haciendo sign-in.
**Nivel:** empieza aquí (guía de plataforma) · **Tiempo:** ~10 minutos hasta la primera App
**Fuente:** [Introducing Devin Apps](https://devin.ai/blog/devin-apps) (13 nov 2026)

## Qué es

Una Devin App es una aplicación web en vivo y privada alojada directamente en la máquina cloud de Devin. Describes la herramienta, Devin la construye, tu equipo la abre desde un enlace — sin hosting, sin pipeline de deploy. Como corre *en* la máquina de Devin, alcanza tus MCPs, integraciones, codebase y su propia base de datos (SQLite/Postgres en la misma box), y llama a la propia API de Devin.

## Construir una

1. Sidebar → **Apps** → describe lo que la App debe hacer (o elige una plantilla de prompt: dashboard de métricas, estado de proyecto, cola de review) → **Build with Devin**
2. Devin hace preguntas de aclaración en la sesión, construye y la pone online — la página de Apps muestra su URL, estado `Building` hasta que la v1 esté en el aire
3. **Share** — copia el enlace; dale alcance a personas nombradas, tu org o tu enterprise. Las Apps nunca son públicas; abrir una exige sign-in en Devin

También puedes decir "publish this as an App" dentro de cualquier sesión que produjo un browser preview.

## Bucle de actualización

- **Edit in session** en la página de la App → describe el cambio → Devin construye una nueva versión en la misma URL. Cada actualización es un despliegue versionado; si una versión nueva falla al arrancar, la anterior sigue sirviendo.
- **Mantenida fresca por automatización:** cablea una automatización (Guía 6) para redesplegar en horario o en cambios de rama — un dashboard que trae datos frescos cada mañana es el uso canónico.

## Cómo corren (las partes que importan)

- **Hibernación:** las Apps se construyen sobre snapshots de memoria — la máquina duerme cuando no se usa, despierta al abrir (la primera carga puede tardar unos segundos). La facturación sigue el tiempo despierto.
- **Stack:** cualquier cosa sirviendo HTTP en un puerto; DB co-localizada en la máquina.
- **Frontera de escala:** una máquina — genial para herramientas internas y dashboards, **no** para servicios de producción de alto tráfico.

## Los tres usos probados

| Uso | Ejemplo |
| --- | --- |
| Herramientas internas | Paneles admin, formularios de solicitud, colas de aprobación — los asesinos de la hoja de cálculo compartida |
| Dashboards | Boards de métricas/soporte/ventas trayendo de tus fuentes de datos, refrescados en horario |
| Copias beta/staging | Tu stack real (frontend+backend+DB+workers) corriendo en la máquina de Devin — compañeros abren una copia de staging desde un enlace |

## Checklist de verificación

- [ ] La App carga en su URL estable después de que la máquina durmiera (espera un cold start de unos segundos)
- [ ] Un cambio por edit-in-session produjo una nueva versión en la misma URL
- [ ] El alcance de compartición es correcto: un compañero sin acceso es detenido en el sign-in

## Trampas

- **Tráfico de producción.** Una máquina, duerme cuando está ociosa — no apuntes usuarios a ella; apunta a tu equipo.
- **Pensamiento estático.** El poder de una App es que *vive en el entorno de Devin* — conéctala a tus datos/MCPs, o has construido una Vercel más débil.

## Prueba de conocimiento

1. ¿Cuál es la diferencia entre una Devin App y un PR preview? *(La App se sirve en vivo desde la máquina de Devin en una URL estable — stateful, persistente, con gate de sign-in — no un artefacto de build.)*
2. ¿Por qué importa "tu equipo la abre haciendo sign-in" para herramientas internas? *(La auth se hereda de la org — sin sistema de login separado que construir o asegurar.)*
3. ¿Qué clase de herramienta interna encaja mejor en Apps? *(Dashboards y superficies de staging donde "bastante bueno ahora" vence a "perfecto después" — el coste de mantenimiento es casi cero.)*

## Fuentes

- [Introducing Devin Apps](https://devin.ai/blog/devin-apps)
- Relacionado: [Guía 6 — Automatizaciones orientadas a eventos](automations-101-event-driven.md) para refresco programado
