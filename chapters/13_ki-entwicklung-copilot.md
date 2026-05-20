# Kapitel 13 – KI-Entwicklung & Copilot-Workflows

## Überblick

Alle WAMOCON-Projekte sind für KI-gestützte Entwicklung mit **GitHub Copilot** optimiert.
Jedes App-Repository enthält vorkonfigurierte Agents, Instructions und globale Copilot-Regeln.

## Copilot-Konfigurationsstruktur

```text
.github/
├── copilot-instructions.md        # Globale Regeln (für jede Copilot-Interaktion)
├── instructions/
│   ├── nextjs.instructions.md     # Next.js 16 App Router Regeln
│   ├── tailwind.instructions.md   # Tailwind CSS v4 Regeln
│   ├── typescript.instructions.md # TypeScript Strict Mode Regeln
│   └── supabase.instructions.md   # Supabase Client, RLS, Migrations
└── agents/
    ├── planner.agent.md           # @planner – Planung ohne Code
    ├── developer.agent.md         # @developer – Implementierung mit Verifikation
    └── reviewer.agent.md          # @reviewer – Code-Review vor dem PR
```text
## Die drei Copilot-Agents

### `@planner` — Technische Planung

**Wann verwenden:**
- Vor dem Start eines neuen Features
- Wenn Anforderungen unklar sind
- Vor Refactoring oder Migrations-Aufgaben

**Was er tut:**
- Codebase erkunden und Kontext sammeln
- Betroffene Dateien und Module identifizieren
- Nummerierten Implementierungsplan erstellen
- **Schreibt keinen Code**

**Beispiel:**

```text
@planner Analysiere, was für eine Authentifizierungsseite mit Supabase
benötigt wird. Erstelle einen nummerierten Implementierungsplan.
```text
---

### `@developer` — Strukturierte Implementierung

**Wann verwenden:**
- Nach der Planung mit `@planner`
- Zur Implementierung von Features, Seiten, API-Routes
- Für Datenbankänderungen und Migrationen

**Vierphasiger Prozess:**

1. **Vorbereitung** — Plan lesen, Codebase verstehen
2. **Implementierung** — Schrittweise, Fehler sofort beheben
3. **Verifikation (Pflicht)** — `typecheck` → `lint` → `build` → lokal testen
4. **Dokumentation** — Handbuch bei Bedarf aktualisieren

**Beispiel:**

```text
@developer Implementiere diesen Plan: [Plan aus @planner einfügen]
```text
---

### `@reviewer` — Code-Review vor dem PR

**Wann verwenden:**
- Bevor ein PR erstellt wird
- Nach einer Implementierung zur Qualitätsprüfung
- Zur Sicherheits- und Performance-Analyse

**Was er tut:**
- Strukturierte Checkliste (Code-Qualität, Next.js 16, Supabase-Sicherheit, Styling)
- Alle Checks ausführen (`typecheck`, `lint`, `build`)
- Review-Bericht mit Status (✅ / ⚠️ / ❌)

**Beispiel:**

```text
@reviewer Überprüfe die Änderungen in src/app/dashboard/ vor dem PR.
```text
---

## Empfohlener Workflow

```text
@planner  →  @developer  →  @reviewer  →  PR erstellen
```text
1. `@planner`: Aufgabe analysieren und Implementierungsplan erstellen lassen
2. `@developer`: Plan übergeben und implementieren lassen
3. `@reviewer`: Code prüfen lassen, Review-Bericht lesen
4. PR erstellen (erst wenn @reviewer keine kritischen Probleme meldet)

## Instructions — Datei-spezifische Regeln

Instructions werden automatisch geladen, wenn Copilot an Dateien arbeitet, die dem `applyTo`-Glob-Muster entsprechen:

| Datei | Gilt für | Inhalt |
| --- | --- | --- |
| `nextjs.instructions.md` | `**/*.tsx, **/*.ts` | Next.js 16 App Router Patterns, async APIs, Server/Client Components |
| `tailwind.instructions.md` | `**/*.tsx, **/*.css` | Tailwind CSS v4 Utility-First, Responsive Design |
| `typescript.instructions.md` | `**/*.ts, **/*.tsx` | Strict Mode, Naming Conventions, Type Safety |
| `supabase.instructions.md` | `**/supabase/**, **/*supabase*` | Client Setup, RLS, Migrations, Schema |

### Eigene Instruction erstellen

```markdown
---
applyTo: "**/*.tsx"
---
# Deine projektspezifischen Regeln hier
```text
## Supabase MCP — Datenbankkontext für Copilot

Der **Supabase MCP (Model Context Protocol) Server** gibt Copilot Zugriff auf das echte Datenbankschema. Damit generiert Copilot akkuraten Code statt Tabellenstrukturen zu raten.

### VS Code Setup (Workspace-Ebene)

`.vscode/mcp.json` anlegen:

```json
{
  "servers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref",
        "dein-project-ref"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "dein-access-token"
      }
    }
  }
}
```text
### VS Code Setup (Benutzer-Ebene, gilt für alle Repos)

In VS Code User Settings (`settings.json`) unter `"mcp"` eintragen — Struktur wie oben.

### Access Token generieren

1. [supabase.com/dashboard/account/tokens](https://supabase.com/dashboard/account/tokens)
2. **Generate new token** → Name vergeben (z. B. „MCP - Local Dev")
3. Token kopieren (wird nur einmal angezeigt)

### MCP-Verbindung testen

Im Copilot-Chat:

```text
Nutze MCP für Datenbank <project-ref>. Liste alle Schemas und Tabellen auf.
```text
MCP aktiviert folgende Fähigkeiten in Copilot:

| Fähigkeit | Beispiel-Prompt |
| --- | --- |
| Tabellen auflisten | „Welche Tabellen gibt es im test-Schema?" |
| Tabelle beschreiben | „Zeig mir die Spalten der orders-Tabelle" |
| SQL generieren | „Schreib eine Abfrage für alle offenen Bestellungen mit Nutzerinfo" |
| Server Action scaffolden | „Erstelle eine Server Action, die das Nutzerprofil per ID lädt" |
| RLS-Policy generieren | „Erstelle eine RLS-Policy, sodass Nutzer nur ihre eigenen Daten sehen" |

### Sicherheitsregeln für MCP

- Immer `--read-only` verwenden (außer wenn Schreibzugriff explizit benötigt)
- Token nie committen — in User-Level-Settings oder Umgebungsvariablen ablegen
- `test`-Schema für KI-unterstützte Entwicklung verwenden, nicht `prod`
- Alle generierten SQL-Statements vor der Ausführung prüfen
- Tokens regelmäßig rotieren

## Copilot-Instruktionen auf Benutzerebene

Jeder Entwickler kann persönliche Copilot-Instructions definieren, die für alle Repos gelten:

**Windows-Pfad:**
```text
C:\Users\<user>\AppData\Roaming\Code\User\prompts\my-default.instructions.md
```text
**Beispiel-Inhalt:**

```markdown
---
description: "Gilt für alle Repos"
---
- Immer TypeScript strict mode einhalten
- Für Datenbankaufgaben MCP mit dem korrekten project-ref nutzen
- Minimale, sichere Änderungen bevorzugen
- Annahmen kommentieren
```text
## Fehlerbehebung bei Copilot-Problemen

| Problem | Lösung |
| --- | --- |
| Agent ignoriert Instructions | `applyTo`-Glob-Muster prüfen — ggf. breiter setzen (`**/*.ts` statt `src/**/*.ts`) |
| Agent überspringt typecheck/lint | In `.agent.md` die Anweisung verschärfen: „muss" statt „sollte" |
| Agent schreibt schlechten Next.js-Code | Konkretes Code-Beispiel in `nextjs.instructions.md` hinzufügen |
| Agent „vergisst" Kontext | Neues Chat-Fenster öffnen, Plan explizit übergeben |
| Agent antwortet auf Englisch | In `copilot-instructions.md` hinzufügen: „Antworte immer auf Deutsch." |
| Agent macht ungebetene Änderungen | In `.agent.md` unter „Rules": „Ändere nur Dateien, die explizit im Plan stehen." |

## Referenzen

- [GitHub Copilot Customization Docs](https://docs.github.com/en/copilot/customizing-copilot)
- [awesome-copilot](https://github.com/github/awesome-copilot) — Beispiele und Best Practices
- `Wamocon/github_workflow` → `docs/github-copilot-guide.md`
- `Wamocon/github_workflow` → `docs/mcp-setup.md`
