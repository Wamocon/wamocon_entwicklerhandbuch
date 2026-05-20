# Kapitel 09 – Jira & Aufgabenmanagement

## Einsatz: Wann ist Jira verpflichtend?

| Projekttyp | Jira-Nutzung |
| --- | --- |
| **Wellen-Appentwicklung** (kleine, schnelle Apps im Wellen-Rhythmus) | **Optional** — empfohlen, aber nicht verpflichtend |
| **Große Projekte** (nicht im Wellen-Rhythmus, längere Laufzeit) | **Verpflichtend** |

Bei Wellen-Apps kann die Aufgabenverwaltung auch über GitHub Issues oder direkt über Copilot-Pläne erfolgen.

## Jira-Ticket-Erstellung

Automatisierte Ticket-Erstellung via [`wamocon_Jira_Ticket_Creation`](https://github.com/Wamocon/wamocon_Jira_Ticket_Creation) (Python).

### Ticket-Typen

| Typ | Verwendung |
| --- | --- |
| **Story** | Neue Funktion aus Nutzersicht beschrieben |
| **Task** | Technische Aufgabe ohne direkten Nutzernutzen |
| **Bug** | Fehlverhalten in einer bestehenden Funktion |
| **Sub-Task** | Teilaufgabe einer Story oder Task |
| **Hotfix** | Kritischer Produktionsfehler, sofort beheben |

### Verlinkung mit GitHub

Ticket-Nummer im Branch-Namen oder PR-Titel angeben:

```text
feature/WMC-123-login-seite
fix/WMC-456-berechnung-korrigieren
```text
## Status-Workflow

```text
Backlog → To Do → In Progress → In Review → Done
```text
| Status | Bedeutung |
| --- | --- |
| **Backlog** | Idee/Anforderung, noch nicht priorisiert |
| **To Do** | Priorisiert, wartet auf Bearbeitung |
| **In Progress** | Entwickler arbeitet aktiv daran |
| **In Review** | PR ist offen, Code-Review läuft |
| **Done** | PR gemergt, Feature ist live |

## ARGUS Review Pipeline

Die [ARGUS Review Pipeline](https://github.com/Wamocon/ARGUS) ist ein Multi-Agenten-Review-System für Inhalte und Anforderungen.

Einsatz:
- Qualitätskontrolle vor Freigabe von Entwicklungsartefakten
- Review von Anforderungsdokumenten
- Prüfung von KI-generierten Outputs

## Standard-Prozessablauf

Verbindliche Vorlage für alle Entwicklungsprojekte:

🔗 **[wamocon.github.io/standard_prozessablauf/](https://wamocon.github.io/standard_prozessablauf/)**

Repo: [`Wamocon/standard_prozessablauf`](https://github.com/Wamocon/standard_prozessablauf)

## Prioritäten

| Priorität | Reaktionszeit | Beschreibung |
| --- | --- | --- |
| **Kritisch** | Sofort | Produktionsausfall oder Datenverlust |
| **Hoch** | Innerhalb 24h | Wichtige Funktion defekt, kein Workaround |
| **Mittel** | Nächster Sprint | Einschränkung mit Workaround |
| **Niedrig** | Nach Kapazität | Nice-to-have, kein Nutzerimpact |

## Sprint-Planung (bei großen Projekten)

Entwicklung in zweiwöchigen Sprints:

1. **Sprint Planning** — Tickets aus dem Backlog in den Sprint ziehen, Aufwände schätzen
2. **Daily Standup** — Kurzes Update: Was wurde gemacht? Was kommt? Gibt es Hindernisse?
3. **Sprint Review** — Fertige Features präsentieren
4. **Retrospektive** — Was lief gut? Was kann verbessert werden?
