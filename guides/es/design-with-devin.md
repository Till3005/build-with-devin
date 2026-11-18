# Guía 8 — Diseño & trabajo visual

**Objetivo:** usar Devin como tu director de arte e implementador para diseño visual de producción — imágenes generadas, sistemas de animación, tipografía — solo por conversación.
**Nivel:** intermedio
**Implantación de origen:** la landing page de **Spraycash** — todo el sistema visual de un sitio fintech diseñado dentro del chat de Devin con Kimi K3, todos los prompts publicados: hero imagery, animaciones de nubes en capas, anillo SVG draw-on, sistema tipográfico de tres fuentes.
**Fuentes:** [relato completo con prompts](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f)

## El patrón

El diseño-via-agente falla cuando los prompts describen *vibes* ("hazlo premium"). Funciona cuando diriges arte como un director creativo: **referencias, restricciones y un bucle de crítica**. La ventaja de Devin sobre una herramienta de diseño es que produce la *implementación* — la animación es código, las imágenes se generan y se colocan, el sistema tipográfico es CSS entregado.

```text
brief + referencias ──► Devin produce assets visuales + código
        ▲                        │
        └──── bucle de crítica: "la animación del anillo dibuja demasiado
              rápido, baja el easing del stroke-dashoffset a 1.4s" ────┘
```

## Paso 1 — Brief como un director creativo

Los prompts del relato de Spraycash comparten una forma — sustantivos concretos, sin adjetivos-de-gusto:

```text
Hero section: dark navy (#0A1628) background, a circular progress ring
as the visual anchor — SVG stroke-dashoffset draw-on animation over
1.4s ease-out, layered clouds behind it drifting on separate
translateX loops at 40s/60s/90s periods so the parallax never repeats.
```

Dale: hexes de la paleta, el mecanismo de la animación (no "haz que se anime"), valores de timing, orden de capas.

## Paso 2 — Bloquea el sistema tipográfico antes que los píxeles

Spraycash cerró un **sistema de tres fuentes** pronto — display, cuerpo, mono — antes de tocar componentes. Haz lo mismo; es la decisión visual de mayor apalancamiento:

```text
Type system: <display font> for hero + section heads, <body font> for
prose, <mono> for numbers/labels. Set the scale: 64/40/28/18/14.
Nothing else uses another size.
```

## Paso 3 — Genera imágenes dentro de la sesión

Devin genera y coloca assets — no uses foto de stock en una página diseñada. El relato muestra hero imagery generada que casa con la paleta del brief. Mantén los assets generados consistentes fijando la directiva de estilo una vez (paleta, iluminación, material) y reusándola en cada petición de asset.

## Paso 4 — Anima con mecanismos, no adjetivos

| Vago (falla) | Mecánico (funciona) |
| --- | --- |
| "entrada suave" | "stagger children 80ms, translateY(12px)→0, opacity 0→1, 400ms ease-out" |
| "parallax sutil" | "tres capas, bucles translateX en períodos de 40/60/90s" |
| "dibuja el anillo" | "stroke-dasharray = circunferencia, animar dashoffset C→0 en 1.4s" |

El anillo, las nubes y los reveals escalonados de Spraycash se especificaron todos a este nivel — y se entregaron como CSS/SVG real, no mockups.

## Paso 5 — El bucle de crítica es el oficio

La lección real del relato: la calidad vino de *iteraciones* — "el anillo dibuja demasiado rápido", "las nubes se leen como ruido, baja la opacidad 30%", "fuente mono en los números". Presupuesta 3–5 rondas de crítica por ancla visual. Devin sostiene la página entera en contexto; cada ronda es un mensaje, no un ticket.

## Checklist de verificación

- [ ] La página renderiza con *cero* imágenes de stock — todos los assets generados o codificados
- [ ] Cada animación es un mecanismo nombrado con valores de timing en el CSS
- [ ] Un sistema tipográfico, una escala — sin tamaños sueltos
- [ ] Vista en 3+ anchos, nada se rompe ni se corta

## Trampas

- **Prompts de adjetivos.** "Premium", "sleek", "modern" dan slop. Los mecanismos y valores dan oficio.
- **One-shot.** Aceptar la primera renderización es por lo que las páginas hechas por agente parecen hechas por agente. La calidad vive en el bucle de crítica.
- **Perder el lock-down.** Define paleta + sistema tipográfico como restricciones *primero*; los assets generados antes de las restricciones nunca casan después.

## Prueba de conocimiento

1. ¿Por qué el autor de Spraycash publicó cada prompt literal? *(La secuencia de prompts *es* el artefacto de diseño — la dirección de arte por conversación solo es reproducible si la conversación lo es.)*
2. ¿Qué requiere "imagen generada + animación en capas" que un mock de screenshot no requiere? *(Assets entregables y un sistema de animación funcionando — la verificación es una página renderizada, no la foto de una.)*
3. ¿Cuándo la dirección por chat es mejor que una herramienta de diseño para landing pages? *(Cuando la salida debe ser código de producción de todos modos — la sesión de diseño *es* la implementación.)*

## Fuentes

- [Designing the Spraycash UI with Kimi K3 in Devin](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f) — prompts completos e historial de iteración
- Relacionado: [built-with-devin — patterns](https://github.com/Till3005/built-with-devin#patterns--write-ups)
