# Kapitel 4, Jira & Aufgabenmanagement

## Einsatz: Wann ist Jira verpflichtend?

| Projekttyp | Jira-Nutzung |
| --- | --- |
| **Wellen-Appentwicklung** (kleine, schnelle Apps im Wellen-Rhythmus) | **Optional**, empfohlen, aber nicht verpflichtend |
| **Große Projekte** (nicht im Wellen-Rhythmus, längere Laufzeit) | **Verpflichtend** |

Bei Wellen-Apps kann die Aufgabenverwaltung auch über GitHub Issues oder direkt über Copilot-Pläne erfolgen.

## Jira-Ticket-Erstellung

Automatisierte Ticket-Erstellung via [`wamocon_Jira_Ticket_Creation`](https://github.com/Wamocon/wamocon_Jira_Ticket_Creation) (Python).

### Ticket-Typen (optional, empfohlener Standard)

| Typ | Verwendung |
| --- | --- |
| **Story** | Neue Funktion aus Nutzersicht beschrieben |
| **Task** | Technische Aufgabe ohne direkten Nutzernutzen |
| **Bug** | Fehlverhalten in einer bestehenden Funktion |
| **Sub-Task** | Teilaufgabe einer Story oder Task |

Die Ticket-Typen sind ein empfohlener Standard. Abweichungen sind projektspezifisch möglich.

## Status-Workflow

```
Backlog → To Do → In Progress → In Review → Done
```

| Status | Bedeutung |
| --- | --- |
| **Backlog** | Idee/Anforderung, noch nicht priorisiert |
| **To Do** | Priorisiert, wartet auf Bearbeitung |
| **In Progress** | Entwickler arbeitet aktiv daran |
| **In Review** | PR ist offen, Code-Review läuft |
| **Done** | PR gemergt, Feature ist live |

## Jira GitHub Integration

Durch die Verlinkung von GitHub und Jira werden Jira-Tickets automatisch aktualisiert,
sobald ein Branch oder Pull Request erstellt wird.

### Branch-Name und Ticket-Nummer

Um die automatische Verknüpfung zu aktivieren, muss die Jira-Ticket-Nummer im Branch-Namen enthalten sein:

```
feature/WMC-123-login-seite
fix/WMC-456-berechnung-korrigieren
```

### Jira Automation: Automatische Statusübergänge

| Aktion in GitHub | Ticket-Status in Jira |
| --- | --- |
| Branch mit Ticket-Nummer erstellt | **In Arbeit** |
| Pull Request geöffnet | **In Review** |
| Pull Request gemergt | **Fertig** |

Die Statusübergänge sind über Jira Automation konfiguriert und laufen automatisch ohne manuellen Eingriff.

## Standard-Prozessablauf

Verbindliche Vorlage für alle Entwicklungsprojekte:

**[wamocon.github.io/standard_prozessablauf/](https://wamocon.github.io/standard_prozessablauf/)**

Repo: [`Wamocon/standard_prozessablauf`](https://github.com/Wamocon/standard_prozessablauf)
