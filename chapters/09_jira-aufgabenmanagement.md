# Kapitel 09 – Jira & Aufgabenmanagement

## Rolle von Jira bei WAMOCON

Jira wird als zentrales Aufgabenmanagement-Tool für die Planung, Priorisierung und Nachverfolgung von Entwicklungsaufgaben eingesetzt. Es dient als Schnittstelle zwischen Produktidee und technischer Umsetzung.

## Verknüpfung mit GitHub

Pull Requests werden mit Jira-Tickets verknüpft, indem die Ticket-Nummer im Branch-Namen oder in der PR-Beschreibung genannt wird:

```
feature/WMC-123-login-seite
fix/WMC-456-berechnung-korrigieren
```

In der PR-Beschreibung sollte immer eine Referenz auf das Jira-Ticket stehen:

```
Closes WMC-123

Änderungen:
- Login-Seite hinzugefügt
- Supabase Auth integriert
```

## Tickettypen

| Typ | Verwendung |
|---|---|
| **Story** | Neue Funktion aus Nutzersicht beschrieben |
| **Task** | Technische Aufgabe ohne direkten Nutzernutzen |
| **Bug** | Fehlverhalten in einer bestehenden Funktion |
| **Hotfix** | Kritischer Produktionsfehler, der sofort behoben werden muss |
| **Epic** | Übergreifendes Thema, das mehrere Stories/Tasks umfasst |

## Status-Workflow

```
Backlog → To Do → In Progress → In Review → Done
```

| Status | Bedeutung |
|---|---|
| **Backlog** | Idee/Anforderung, noch nicht priorisiert |
| **To Do** | Priorisiert, wartet auf Bearbeitung |
| **In Progress** | Entwickler arbeitet aktiv daran |
| **In Review** | PR ist offen, Code-Review läuft |
| **Done** | PR gemergt, Feature ist live |

## Sprint-Planung

Entwicklung erfolgt in **zweiwöchigen Sprints**:

1. **Sprint Planning** — Tickets aus dem Backlog in den Sprint ziehen, Aufwände schätzen
2. **Daily Standup** — Kurzes tägliches Update: Was wurde gemacht? Was kommt? Gibt es Hindernisse?
3. **Sprint Review** — Fertige Features werden präsentiert
4. **Retrospektive** — Was lief gut? Was kann verbessert werden?

## Konventionen für Ticket-Beschreibungen

Ein gutes Ticket enthält:

- **Zusammenfassung**: Kurze, klare Beschreibung (max. eine Zeile)
- **Akzeptanzkriterien**: Wann gilt das Ticket als erledigt?
- **Technische Hinweise**: Betroffene Dateien, API-Endpunkte, Datenbankänderungen
- **Verknüpfte Tickets**: Abhängigkeiten zu anderen Tickets

## WMC-Anforderungsportal

Das Repository `Wamocon/WMC-Anforderungsportal` ist ein separates Tool zur Sammlung von Kundenanforderungen.
Anforderungen aus dem Portal werden nach Bewertung in Jira-Tickets überführt.

## Prioritäten

| Priorität | Reaktionszeit | Beschreibung |
|---|---|---|
| **Kritisch** | Sofort | Produktionsausfall oder Datenverlust |
| **Hoch** | Innerhalb 24h | Wichtige Funktion defekt, kein Workaround |
| **Mittel** | Nächster Sprint | Einschränkung mit Workaround |
| **Niedrig** | Nach Kapazität | Nice-to-have, kein Nutzerimpact |
