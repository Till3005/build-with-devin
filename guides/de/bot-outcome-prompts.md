# Bot-Outcome-Prompts, seziert

**Ziel:** Outcome-Prompts so schreiben, wie die dokumentierten Deployments es tatsächlich taten — Ownership eines Bereichs, keine Aufgabenliste.
**Level:** mittel · **Zeit:** 20 Min. zum Entwerfen, eine Woche zum Kalibrieren

Jedes öffentliche Bot-Deployment, das große Zahlen lieferte, begann mit einem kurzen Prompt, der ein *Ergebnis* zuwies. Dieser Leitfaden sammelt die echten und reverse-engineert, warum sie funktionieren.

## Das Musterbeispiel

> *"your job is to product manage the android app"*

Der gesamte Auftrag des Android Bot. Ein Satz produzierte 44 Tage selbstgesteuerter Arbeit: Der Bot zerlegte das Ergebnis in selbst geschriebene Tickets, fuhr eine Devin-Session pro Ticket und lieferte 1.134 gemergte PRs ([Launch-Post](https://devin.ai/blog/introducing-devin-bots)). Beachte, was der Prompt **nicht** enthält: keine Ticketliste, keine Akzeptanzkriterien, keinen Zeitplan. Das Ergebnis selbst impliziert sie alle.

## Die Anatomie eines funktionierenden Outcome-Prompts

| Element | Was es tut | Beispiel |
| --- | --- | --- |
| **Eine Rolle** | Sagt dem Bot, wie er sich *verhalten* soll, nicht nur was er produzieren soll | "product manage", "own the QA of onboarding flows" |
| **Eine begrenzte Oberfläche** | Ein Scope, den der Bot vollständig übersehen kann — eine App, ein Check, eine Datenquelle | "the android app", "layout regressions", "30+ onboarding flows" |
| **Eine implizite Definition-of-done** | Ein Zustand, gegen den sich der Bot selbst verifizieren kann | "feature parity with iOS", "no layout-shift regressions", "every flow green" |
| **Dauerhafte Autorität** | Der Bot entscheidet *wann* und *was als Nächstes* — das macht ihn zum Bot, nicht zum Skript | "your job is to…", "keep…", "watch for…" |

## Muster aus dem offiziellen Template-Marketplace

Die 16 [Marketplace-Templates](https://devin.ai/bots/templates) folgen alle derselben Grammatik. Wiederverwendbare Formulierungen, verallgemeinert:

**Ownership einer Domäne** — "Find bugs, improvements, performance and refactoring work in a named product area; open one small PR at a time with proof it works." (Software Factory)

**Ownership eines Checks** — "Every 3 hours, build production main, simulate first/repeat/deferred visits, and file fixes with before/after videos for any regression you introduce—or find." (Layout-Bot-Muster)

**Ownership einer Lebenszyklus-Stufe** — "Take a ticket or an ask to a tested PR and through review." (Product Engineer)

**Ownership einer Kadenz** — "Weekly: remove dead code, one safe PR per round." (Code Reaper) — geplante Ergebnisse werden als Rhythmus formuliert, nicht als Auslöser.

**Ownership des Team-Metabolismus** — "Watch the channels, post updates, hand work to the right teammate, follow up until done." (Chief of Staff)

**Ownership der Hygiene** — "Old flags, stale deps, CVEs — turned into small safe PRs." (Code Health Engineer)

## Multi-Bot-Orgs: Prompts, die Autorität gewähren

In Flotten (SuperJennyStack, Frankie, tigsbot) enthält der Prompt des Chief-Bots den *Routing-Vertrag*: welcher Bot welche Oberfläche besitzt und wann nach oben statt seitwärts eskaliert wird. Der eigentliche Prompt des Menschen ist die Roll-up-Spec: "bring me every open decision in one thread." Siehe [Leitfaden 4](bots-203-multi-bot-org.md) für das volle Organigramm.

## Anti-Muster

- **Task-förmige Prompts.** "Fix these 12 issues" — der Bot wird fertig und idlet; du bekommst eine Session, keinen Bot.
- **Nicht verifizierbare Ergebnisse.** "Make the app better" — ohne Selbst-Check ist der einzige Ausgang des Bots Needs-you-Spam.
- **Versteckter Scope.** Wenn das Ergebnis Systeme braucht, die der Bot nicht sieht (ein Staging, das er nicht erreicht, ein Dashboard, das er nicht lesen kann), bleibt er entweder stecken oder halluziniert Fortschritt. Gib ihm die Oberfläche oder schrumpfe das Ergebnis.
- **Keine Merge-Authority-Story.** Die 88 % Self-Merge-Rate existiert, weil CI und Review-Gates für autonome Merges vorkonfiguriert waren. Sage es: "merge when CI is green and diff < N lines" oder "always open as draft for human review."

## Deinen entwerfen — der Drei-Zeilen-Test

Ein guter Outcome-Prompt beantwortet, in dieser Reihenfolge:

1. **Was ist deins?** — die Oberfläche
2. **Wie sieht gut aus?** — der verifizierbare Zustand
3. **Was tust du dagegen?** — das dauerhafte Verhalten

Wenn ein Fremder die Wahrheit von Zeile 2 nicht von außen prüfen könnte, verschärfe sie.

## Verifizieren

- [ ] Nimm ein echtes Backlog-Item aus deinem Repo und schreibe es als Outcome-Prompt um — Oberfläche, verifizierbarer Zustand, dauerhaftes Verhalten
- [ ] Zeig es jemandem, der den Codebase nicht kennt: Könnte er von außen sagen, wann der Bot "gewinnt"?
- [ ] Die erste Antwort des Bots sollte ein Plan oder Klärungsfragen zum Scope sein — fragt er "was soll ich zuerst tun", hat der Prompt keine Ownership zugewiesen

## Fallstricke

- **Eine Aufgabenliste im Ergebnis-Kostüm.** "Do X, then Y, then Z" ist immer noch eine Checklist — der Bot kann nicht repriorisieren, wenn sich die Welt ändert.
- **"Keep the app good" ohne Definition von gut.** Ohne verifizierbaren Zustand wählt der Bot einen — und es wird nicht deiner sein.
- **Scope breiter als eine Oberfläche.** "Own engineering" scheitert; "own the iOS app" liefert. Teile danach, was ein einzelner Außenstehender vollständig beobachten könnte.

## Wissenscheck

1. Warum funktioniert "own the Android app" besser als "fix Android bugs"? *(Ownership impliziert dauerhaftes Urteil — der Bot entscheidet, welche Bugs zählen, nicht nur ob gefixt wird.)*
2. Was ist falsch an "make the CI fast"? *(Von außen nicht verifizierbar — keine Schwelle. "CI under 8 minutes" ist es.)*
3. Welche der drei Fragen beantwortet "text me if tests fail"? *(Dauerhaftes Verhalten — es sagt, was der Bot über den Zustand tut, nichts über Oberfläche oder Ziel.)*

## Quellen

- [Introducing Devin Bots](https://devin.ai/blog/introducing-devin-bots) · [Bots-Doku](https://docs.devin.ai/work-with-devin/bots) · [Template-Marketplace](https://devin.ai/bots/templates)
- Deployment-Berichte verlinkt in [built-with-devin](https://github.com/Till3005/built-with-devin#documented-deployments)
