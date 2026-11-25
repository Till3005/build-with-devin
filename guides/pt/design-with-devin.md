# Guia 8 — Design & trabalho visual

**Objetivo:** usar o Devin como seu diretor de arte e implementador para design visual de produção — imagens geradas, sistemas de animação, tipografia — só por conversa.
**Nível:** intermediário
**Implantação de origem:** a landing page do **Spraycash** — todo o sistema visual de um site fintech desenhado dentro do chat do Devin com Kimi K3, todos os prompts publicados: hero imagery, animações de nuvens em camadas, anel SVG draw-on, sistema tipográfico de três fontes.
**Fontes:** [relato completo com prompts](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f)

## O padrão

Design-via-agente falha quando prompts descrevem *vibes* ("faça premium"). Funciona quando você dirige arte como um diretor criativo: **referências, restrições e um loop de crítica**. A vantagem do Devin sobre uma ferramenta de design é que ele produz a *implementação* — a animação é código, as imagens são geradas e posicionadas, o sistema tipográfico é CSS entregue.

```text
brief + referências ──► Devin produz assets visuais + código
        ▲                        │
        └──── loop de crítica: "a animação do anel desenha rápido demais,
              desacelere o easing do stroke-dashoffset para 1.4s" ─────┘
```

## Passo 1 — Brief como um diretor criativo

Os prompts do relato do Spraycash compartilham uma forma — substantivos concretos, sem adjetivos-de-gosto:

```text
Hero section: dark navy (#0A1628) background, a circular progress ring
as the visual anchor — SVG stroke-dashoffset draw-on animation over
1.4s ease-out, layered clouds behind it drifting on separate
translateX loops at 40s/60s/90s periods so the parallax never repeats.
```

Dê a ele: hexes da paleta, o mecanismo da animação (não "faça animar"), valores de timing, ordem de camadas.

## Passo 2 — Tranque o sistema tipográfico antes dos pixels

O Spraycash travou um **sistema de três fontes** cedo — display, corpo, mono — antes de tocar em componentes. Faça o mesmo; é a decisão visual de maior alavancagem:

```text
Type system: <display font> for hero + section heads, <body font> for
prose, <mono> for numbers/labels. Set the scale: 64/40/28/18/14.
Nothing else uses another size.
```

## Passo 3 — Gere imagens dentro da sessão

O Devin gera e posiciona assets — não use foto de stock numa página desenhada. O relato mostra hero imagery gerada casando com a paleta do brief. Mantenha assets gerados consistentes fixando a diretiva de estilo uma vez (paleta, iluminação, material) e reusando-a em cada pedido de asset.

## Passo 4 — Anime com mecanismos, não adjetivos

| Vago (falha) | Mecânico (funciona) |
| --- | --- |
| "entrada suave" | "stagger children 80ms, translateY(12px)→0, opacity 0→1, 400ms ease-out" |
| "parallax sutil" | "três camadas, loops translateX em períodos de 40/60/90s" |
| "desenhe o anel" | "stroke-dasharray = circunferência, animar dashoffset C→0 em 1.4s" |

O anel, as nuvens e os reveals escalonados do Spraycash foram todos especificados nesse nível — e entregues como CSS/SVG real, não mockups.

## Passo 5 — O loop de crítica é o ofício

A lição real do relato: a qualidade veio de *iterações* — "o anel desenha rápido demais", "as nuvens leem como ruído, baixe a opacidade 30%", "fonte mono nos números". Orce 3–5 rodadas de crítica por âncora visual. O Devin segura a página inteira em contexto; cada rodada é uma mensagem, não um ticket.

## Checklist de verificação

- [ ] A página renderiza com *zero* imagens de stock — todos os assets gerados ou codificados
- [ ] Toda animação é um mecanismo nomeado com valores de timing no CSS
- [ ] Um sistema tipográfico, uma escala — sem tamanhos perdidos
- [ ] Vista em 3+ larguras, nada quebra ou corta

## Armadilhas

- **Prompts adjetivados.** "Premium", "sleek", "modern" geram slop. Mecanismos e valores geram ofício.
- **One-shot.** Aceitar a primeira renderização é por que páginas feitas por agente parecem feitas por agente. A qualidade vive no loop de crítica.
- **Perder o lock-down.** Defina paleta + sistema tipográfico como restrições *primeiro*; assets gerados antes das restrições nunca combinam depois.

## Teste de conhecimento

1. Por que o autor do Spraycash publicou cada prompt verbatim? *(A sequência de prompts *é* o artefato de design — direção de arte por conversa só é reproduzível se a conversa for.)*
2. O que "imagem gerada + animação em camadas" exige que um mock de screenshot não exige? *(Assets entregáveis e um sistema de animação funcionando — a verificação é uma página renderizada, não a foto de uma.)*
3. Quando direção por chat é melhor que uma ferramenta de design para landing pages? *(Quando a saída precisa ser código de produção de qualquer forma — a sessão de design *é* a implementação.)*

## Demonstração — brief por mecanismo, refinamento por crítica, no Devin CLI v3000.14 (swe-2-flash-medium)

Uma página fintech crua (`index.html`, fonte padrão), um brief estilo Spraycash com mecanismos reais — paleta em hex, anel `stroke-dashoffset` em 1.4s ease-out, três camadas de nuvens a 40/60/90s, escala de 3 fontes — e uma rodada de crítica com valores exatos. As duas rodadas aconteceram na mesma sessão.

**Vídeo (61 s, sem som):** página crua → brief mecânico → implementação → hero renderizado → crítica → render refinado.

[![De HTML cru a um hero desenhado — brief, render, crítica, re-render](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/walkthrough-poster.webp)](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/walkthrough.mp4)

![1. O ponto de partida — HTML puro, estilo padrão](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step1-bare-page.webp)
*1. Antes: três linhas de texto e um botão*

![2. O relatório de implementação — cada mecanismo nomeado: dashoffset 1131→203.6 em 1.4s, camadas 40/60/90s, escala 56/28/16](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step2-brief-applied.webp)
*2. Os números do brief caíram verbatim no código — mais um fallback de prefers-reduced-motion que ele mesmo adicionou*

![3. Primeiro render — hero navy, anel desenhando a 82%, nuvens à deriva, números em mono](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step3-first-render.webp)
*3. Saída da rodada 1 — CSS/SVG real, não mockup*

![4. A crítica aplicada — nuvens a 12% de opacidade, anel suavizado para #3ECF8E, gap de stats 48px; ele até apontou que o CTA ainda usava o verde antigo](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step4-critique-applied.webp)
*4. O ofício mora na crítica: valores exatos entram, diff exato sai — e ele pegou uma inconsistência que não mencionamos*

![5. Render final — mesma estrutura, equilibrada e sóbria](https://till3005.github.io/built-with-devin/assets/guides/design-with-devin/step5-final-render.webp)
*5. Saída da rodada 2 — a iteração é uma mensagem, não um ticket*

## Fontes

- [Designing the Spraycash UI with Kimi K3 in Devin](https://dev.to/ibrahimpima/designing-the-spraycash-ui-with-kimi-k3-in-devin-4l2f) — prompts completos e histórico de iteração
- Relacionado: [built-with-devin — patterns](https://github.com/Till3005/built-with-devin#patterns--write-ups)
