# Kapitel 00 – Einleitung

## Was ist das WAMOCON Entwicklerhandbuch?

Das WAMOCON Entwicklerhandbuch ist die zentrale Referenz für alle Entwickler, die Apps,
Landing Pages oder Infrastruktur-Projekte innerhalb der WAMOCON Organisation erstellen
und betreiben. Es beschreibt verbindliche Standards, Prozesse und Werkzeuge, die bei
jeder Entwicklung einzuhalten sind.

## Zielgruppe

Dieses Handbuch richtet sich an:

- Entwickler, die mit GitHub Copilot WAMOCON-Apps umsetzen
- Administratoren, die Supabase- oder Vercel-Projekte verwalten
- Alle Beteiligten, die WAMOCON-Prozesse (Wellen-Rhythmus, Jira, Anforderungsdokument)
  anwenden

## Aufbau des Handbuchs

| Kapitel | Thema |
| ------- | ----- |
| 1 | GitHub & Repository-Struktur |
| 2 | Tech Stack & Standards |
| 3 | Entwicklungsprozess |
| 4 | Jira & Aufgabenmanagement |
| 5 | Supabase Cloud Projekt |
| 6 | Vercel Deployment |
| 7 | Sicherheit & Code-Qualität |
| 8 | KI-Entwicklung & Copilot-Workflows |
| 9 | Produkt-Ökosystem & App-Katalog |
| 10 | Glossar & Referenzen |

## Entwicklungsphilosophie

Die gesamte App-Entwicklung bei WAMOCON wird vollständig mit **GitHub Copilot**
durchgeführt. Copilot ist das primäre Entwicklungswerkzeug – von der Planung über
die Implementierung bis hin zu Migrationen und Deployment-Konfigurationen.

Der empfohlene Workflow lautet:

1. **@planner** – Entwicklungsplan aus dem Anforderungsdokument ableiten
2. **@developer** – Plan iterativ mit Copilot umsetzen
3. **@reviewer** – Code-Review und ARGUS-Pipeline durchlaufen
4. **PR erstellen** und auf `main` mergen → automatisches Produktions-Deployment

## Verbindlichkeit

Alle in diesem Handbuch beschriebenen Standards sind verbindlich für jede WAMOCON-App.
Abweichungen bedürfen einer expliziten Entscheidung und Dokumentation im jeweiligen
Projekt-Repository.
