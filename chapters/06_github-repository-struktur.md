# Kapitel 06 – GitHub & Repository-Struktur

## Organisation

Alle WAMOCON-Projekte sind unter der GitHub-Organisation **[Wamocon](https://github.com/Wamocon)** zusammengefasst.
Die Organisation enthält aktuell über 90 Repositories, die sich in drei Hauptkategorien unterteilen:

| Kategorie | Beschreibung | Beispiele |
| --- | --- | --- |
| **Apps** | TypeScript/Next.js-Webanwendungen | `wamohub`, `carman`, `TeamRadar`, `belegbox` |
| **Landing Pages** | Statische HTML-Seiten für Apps | `carman_lp`, `trace_lp`, `away_lp` |
| **Infrastruktur** | Shared Workflows, Templates, Docs | [`github_workflow`](https://github.com/Wamocon/github_workflow), [`localSupabaseDB`](https://github.com/Wamocon/localSupabaseDB), [`template_repo`](https://github.com/Wamocon/template_repo) |

## Infrastruktur-Repositories

### `Wamocon/github_workflow`

Das zentrale CI/CD-Repository der Organisation. Enthält wiederverwendbare GitHub Actions Workflows, die alle Projekte einbinden:

```text
github_workflow/
├── .github/workflows/
│   ├── pr-checks.yml           # TypeScript + ESLint-Validierung (reusable)
│   ├── pr-autofix.yml          # Auto-Fix von Lint- & Formatierungsfehlern (reusable)
│   ├── deploy-preview.yml      # Vercel Preview-Deployment (reusable)
│   └── deploy-production.yml   # Vercel Produktions-Deployment (reusable)
├── examples/
│   ├── caller-pr-pipeline.yml  # Vorlage für PR-Workflow im eigenen Repo
│   └── caller-production-deploy.yml  # Vorlage für Deploy-Workflow
└── docs/
    ├── workflow-guide.md
    ├── supabase-vercel-linking.md
    ├── database-schema-migrations.md
    ├── mcp-setup.md
    ├── github-copilot-guide.md
    └── tips-and-best-practices.md
```text
### `Wamocon/localSupabaseDB`

Template-Repository für lokale Supabase-Entwicklungsumgebungen.
Jede Next.js-App bekommt bei Bedarf eine eigene Kopie, um lokal ohne Supabase Cloud entwickeln zu können.

### `Wamocon/wamohub`

Das Haupt-App-Template der Organisation (intern „relda" genannt). Dient als Ausgangspunkt für alle neuen Next.js-Apps. Enthält vollständige Konfiguration für:
- Next.js 16 App Router
- Supabase-Integration
- GitHub Actions CI/CD
- Copilot-Agents und -Instructions

## Sichtbarkeit und Zugriff

- Alle App-Repositories sind standardmäßig **intern** (nur für Org-Mitglieder sichtbar)
- Landing Pages können je nach Bedarf öffentlich sein
- Repos werden für das initiale Vercel-Deployment **vorübergehend öffentlich** gestellt und danach wieder auf intern gesetzt

## Branch-Strategie

### Standard: main / dev

Der Standardansatz bei allen WAMOCON-Apps:

```text
main   ← Produktions-Branch, immer deploybar, kein direkter Commit
dev    ← Entwicklungs-Branch, aktive Arbeit
```text
- Entwicklung geschieht auf `dev`
- PRs laufen von `dev` → `main` nach Review & Tests
- Direkte Commits auf `main` sind nicht erlaubt

### Themenspezifisches Branching (vereinzelt)

Bei größeren Features oder paralleler Entwicklung können zusätzliche Branches genutzt werden:

```text
feature/auth       ← Neues Feature
fix/bugname        ← Fehlerbehebung
hotfix/kritisch    ← Dringender Produktionsfehler
```text
Diese Branches werden von `dev` abgezweigt und zurück nach `dev` gemergt.

**Grundregel:** Niemals direkt auf `main` commiten — immer über `dev` und dann PR.

## Naming Conventions

| Typ | Konvention | Beispiele |
| --- | --- | --- |
| **App-Repos** | `snake_case`, kleingeschrieben | `backup_planner`, `carman`, `daily_echo` |
| **Landing-Page-Repos** | `[appname]_lp`, kleingeschrieben | `carman_lp`, `trace_lp`, `away_lp` |
| **Infrastruktur-Repos** | `camelCase` | `AppMonitor`, `TeamRadar`, `localSupabaseDB` |

Sonderfälle und Ausnahmen sind im App-Katalog (Kapitel 14) dokumentiert.

## Commit-Konventionen

WAMOCON folgt dem [Conventional Commits](https://www.conventionalcommits.org/) Standard:

```text
feat(auth): Login-Seite hinzufügen
fix(orders): Gesamtberechnung bei Rabatten korrigieren
chore(deps): supabase-js auf v2.45 aktualisieren
db(migration): Tabelle notifications erstellen
ci(workflow): Node.js-Version auf 20 aktualisieren
docs(readme): Deployment-Anleitung ergänzen
style(lint): Formatierungsfehler automatisch behoben
```text
## Repository-Struktur (Standard-App)

Alle App-Repos basieren auf dem `wamohub`-Template und haben diese Struktur:

```text
<app-name>/
├── .github/
│   ├── agents/                 # KI-Personas (@planner, @developer, @reviewer)
│   ├── instructions/           # Datei-spezifische Copilot-Regeln
│   ├── workflows/
│   │   ├── pr-pipeline.yml     # Ruft zentralen Workflow auf
│   │   └── deploy.yml          # Ruft zentralen Deploy-Workflow auf
│   └── copilot-instructions.md # Globale Copilot-Regeln
├── src/
│   └── app/                    # Next.js App Router
├── supabase/
│   └── migrations/             # SQL-Migrationsdateien
├── tests/                      # Playwright E2E-Tests
├── legal-docs/                 # Impressum, Datenschutzerklärung, AGB
├── .env.example                # Template für Umgebungsvariablen
├── HOWTO.md                    # Setup- & Deployment-Guide (DE/EN)
├── AGENTS.md                   # Copilot-Agents Dokumentation
├── package.json
├── tsconfig.json
├── next.config.ts
└── eslint.config.mjs
```text
## Pull Requests

Richtlinien für jeden PR:

1. PRs klein halten — angestrebt unter 400 geänderte Zeilen
2. Einen Fokus pro PR — keine Mischung von Feature und Refactoring
3. Klare Beschreibung: Was wurde geändert und warum?
4. Screenshots bei UI-Änderungen beifügen
5. Erst alle Änderungen pushen, dann den PR öffnen (jeder Push auf offenen PR triggert CI)
6. Immer nur einen offenen PR gleichzeitig haben

## Secrets-Management

| Secret | Scope | Beschreibung |
| --- | --- | --- |
| `VERCEL_TOKEN` | Organisation | Vercel API-Token (org-weit konfiguriert) |
| `VERCEL_ORG_ID` | Organisation | Vercel Organisations-ID (org-weit konfiguriert) |
| `VERCEL_PROJECT_ID` | Repository | Vercel Projekt-ID (pro Repo in Repo-Secrets) |

Supabase-Credentials (URL, Anon Key, Service Role Key) werden als Vercel Environment Variables konfiguriert, nicht als GitHub Secrets.
