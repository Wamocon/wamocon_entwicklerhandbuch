#!/usr/bin/env python3
"""Build script: aktualisiert Markdown-Kapitel und regeneriert index.html"""

import re
import os
import markdown as md_lib

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Neue Markdown-Inhalte
# ---------------------------------------------------------------------------

EINLEITUNG = r"""# Kapitel 00 – Einleitung

## Was ist das WAMOCON Entwicklerhandbuch?

Das WAMOCON Entwicklerhandbuch ist die zentrale Referenz für alle Entwickler, die Apps,
Landing Pages oder Infrastruktur-Projekte innerhalb der WAMOCON Organisation erstellen
und betreiben. Es beschreibt Standards, Prozesse und Werkzeuge, die bei der Entwicklung
empfohlen werden.

## Zielgruppe

Dieses Handbuch richtet sich an:

- Entwickler, die mit GitHub Copilot WAMOCON-Apps umsetzen
- Administratoren, die Supabase- oder Vercel-Projekte verwalten
- Alle Beteiligten, die WAMOCON-Prozesse (Wellen-Rhythmus, Jira, Anforderungsdokument)
  anwenden

## Aufbau des Handbuchs

| Kapitel | Thema |
| ------- | ----- |
| QS | Quickstart |
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
durchgeführt. Copilot ist das primäre Entwicklungswerkzeug, von der Planung über
die Implementierung bis hin zu Migrationen und Deployment-Konfigurationen.

## Verbindlichkeit

Alle in diesem Handbuch beschriebenen Standards sind der empfohlene Ansatz für
WAMOCON-Apps. Abweichungen sind möglich und können im jeweiligen Projekt-Repository
dokumentiert werden.
"""

QUICKSTART = r"""# Quickstart

Eine Kurzübersicht des Standardprozesses von der Idee bis zur Produktion.
Detaillierte Beschreibung jedes Schritts im **[Standard-Prozessablauf](https://wamocon.github.io/standard_prozessablauf/)**.

## Schritt-für-Schritt

1. Produktidee formulieren und Anforderungsdokument erstellen.
2. Anforderungsdokument in OneDrive ablegen und zur Freigabe einreichen.
3. Freigabe abwarten.
4. Supabase Cloud Projekt per E-Mail beantragen (→ Kapitel 5).
5. Domain bei Strato per E-Mail beantragen (→ Kapitel 6).
6. Neues GitHub-Repository aus `template_repo` erstellen, `dev`-Branch anlegen.
7. Anforderungsdokument in GitHub Copilot laden, Entwicklungsplan erstellen lassen.
8. Iterative Implementierung mit Copilot entlang des Plans durchführen.
9. Lokal testen: `npm run typecheck`, `npm run lint`, `npm run dev`.
10. PR von `dev` nach `main` erstellen, Review abwarten, mergen.
11. Vercel Produktions-Deployment läuft automatisch nach dem Merge.
12. Landing Page generieren und über GitHub Pages veröffentlichen.

---

Vollständiger Prozess: **[wamocon.github.io/standard_prozessablauf/](https://wamocon.github.io/standard_prozessablauf/)**
"""

GITHUB = r"""# Kapitel 1 – GitHub & Repository-Struktur

## Organisation

Alle WAMOCON-Projekte sind unter der GitHub-Organisation **[Wamocon](https://github.com/Wamocon)** zusammengefasst.
Die Organisation enthält aktuell über 90 Repositories, die sich in drei Hauptkategorien unterteilen:

| Kategorie | Beschreibung |
| --- | --- |
| **Apps** | TypeScript/Next.js-Webanwendungen |
| **Landing Pages** | Statische HTML-Seiten für Apps |
| **Infrastruktur** | Shared Workflows, Templates, Docs |

### Apps

[accessCheck](https://github.com/Wamocon/accessCheck),
[ai_safeguard](https://github.com/Wamocon/ai_safeguard),
[AppMonitor](https://github.com/Wamocon/AppMonitor),
[ARIA](https://github.com/Wamocon/ARIA),
[auktivo](https://github.com/Wamocon/auktivo),
[away](https://github.com/Wamocon/away),
[backofficeassistent](https://github.com/Wamocon/backofficeassistent),
[backup_planner](https://github.com/Wamocon/backup_planner),
[bedarfspilot](https://github.com/Wamocon/bedarfspilot),
[belegbox](https://github.com/Wamocon/belegbox),
[buyright-ai](https://github.com/Wamocon/buyright-ai),
[cardscan](https://github.com/Wamocon/cardscan),
[carman](https://github.com/Wamocon/carman),
[daily_echo](https://github.com/Wamocon/daily_echo),
[energy](https://github.com/Wamocon/energy),
[ghostaccounts](https://github.com/Wamocon/ghostaccounts),
[grundsteuerPruefer](https://github.com/Wamocon/grundsteuerPruefer),
[ki-prufungstrainer](https://github.com/Wamocon/ki-prufungstrainer),
[KI-Manager-LMS](https://github.com/Wamocon/KI-Manager-LMS),
[kinderpartyplaner](https://github.com/Wamocon/kinderpartyplaner),
[kitaradar](https://github.com/Wamocon/kitaradar),
[KLAR](https://github.com/Wamocon/KLAR),
[ladeKompass](https://github.com/Wamocon/ladeKompass),
[localforge](https://github.com/Wamocon/localforge),
[makeartalanya-app](https://github.com/Wamocon/makeartalanya-app),
[marketing_powerhouse](https://github.com/Wamocon/marketing_powerhouse),
[meine_wohnung](https://github.com/Wamocon/meine_wohnung),
[meinezielcollage](https://github.com/Wamocon/meinezielcollage),
[parzella](https://github.com/Wamocon/parzella),
[plan-it](https://github.com/Wamocon/plan-it),
[realityCheck](https://github.com/Wamocon/realityCheck),
[rideproof](https://github.com/Wamocon/rideproof),
[schufacleaner](https://github.com/Wamocon/schufacleaner),
[Sirin](https://github.com/Wamocon/Sirin),
[skillmapper](https://github.com/Wamocon/skillmapper),
[stammfeuer](https://github.com/Wamocon/stammfeuer),
[TeamRadar](https://github.com/Wamocon/TeamRadar),
[treffpunkt](https://github.com/Wamocon/treffpunkt),
[Universal_Inventory_Manager](https://github.com/Wamocon/Universal_Inventory_Manager),
[Universal-AI-Testing](https://github.com/Wamocon/Universal-AI-Testing),
[ustafix.app](https://github.com/Wamocon/ustafix.app),
[vereinsping](https://github.com/Wamocon/vereinsping),
[vertragsmanager](https://github.com/Wamocon/vertragsmanager),
[wamocon_homepage](https://github.com/Wamocon/wamocon_homepage),
[Wamocon_FIAE](https://github.com/Wamocon/Wamocon_FIAE),
[wamohub](https://github.com/Wamocon/wamohub),
[wartezeit-waechter](https://github.com/Wamocon/wartezeit-waechter),
[wedbudget](https://github.com/Wamocon/wedbudget),
[wg-planer](https://github.com/Wamocon/wg-planer),
[WMC-Anforderungsportal](https://github.com/Wamocon/WMC-Anforderungsportal)

### Landing Pages

[away_lp](https://github.com/Wamocon/away_lp),
[auktivo_lp](https://github.com/Wamocon/auktivo_lp),
[backofficeassistent_lp](https://github.com/Wamocon/backofficeassistent_lp),
[carman_lp](https://github.com/Wamocon/carman_lp),
[dailyecho_lp](https://github.com/Wamocon/dailyecho_lp),
[ghostaccounts_lp](https://github.com/Wamocon/ghostaccounts_lp),
[grundsteuerpruefer_lp](https://github.com/Wamocon/grundsteuerpruefer_lp),
[kitaradar_lp](https://github.com/Wamocon/kitaradar_lp),
[KI-Prufungstrainer_lp](https://github.com/Wamocon/KI-Prufungstrainer_lp),
[ladeKompass_lp](https://github.com/Wamocon/ladeKompass_lp),
[lfa_landing_page](https://github.com/Wamocon/lfa_landing_page),
[LocalForge_lp](https://github.com/Wamocon/LocalForge_lp),
[parzella_lp](https://github.com/Wamocon/parzella_lp),
[plan-it_lp](https://github.com/Wamocon/plan-it_lp),
[rideproof_lp](https://github.com/Wamocon/rideproof_lp),
[schufacleaner_lp](https://github.com/Wamocon/schufacleaner_lp),
[Sirin_lp](https://github.com/Wamocon/Sirin_lp),
[TeamRadar_lp](https://github.com/Wamocon/TeamRadar_lp),
[trace_lp](https://github.com/Wamocon/trace_lp),
[treffpunkt_lp](https://github.com/Wamocon/treffpunkt_lp),
[vereinsping_lp](https://github.com/Wamocon/vereinsping_lp),
[vertragsmanager_lp](https://github.com/Wamocon/vertragsmanager_lp),
[wartezeit-waechter_lp](https://github.com/Wamocon/wartezeit-waechter_lp),
[wg-planer_lp](https://github.com/Wamocon/wg-planer_lp)

### Infrastruktur

[github_workflow](https://github.com/Wamocon/github_workflow),
[localSupabaseDB](https://github.com/Wamocon/localSupabaseDB),
[template_repo](https://github.com/Wamocon/template_repo)

## Infrastruktur-Repositories

### `Wamocon/github_workflow`

Das zentrale CI/CD-Repository der Organisation. Enthält wiederverwendbare GitHub Actions Workflows, die alle Projekte einbinden:

```
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
```

### `Wamocon/localSupabaseDB`

Template-Repository für lokale Supabase-Entwicklungsumgebungen.
Jede Next.js-App bekommt bei Bedarf eine eigene Kopie, um lokal ohne Supabase Cloud entwickeln zu können.

### `Wamocon/template_repo`

Das Basis-Template für alle neuen WAMOCON-Apps. Enthält vollständige Konfiguration für:

- Next.js 16 App Router
- Supabase-Integration
- GitHub Actions CI/CD
- Copilot-Agents und Instructions

## Sichtbarkeit und Zugriff

- Alle App-Repositories sind standardmäßig **intern** (nur für Org-Mitglieder sichtbar)
- Landing Pages können je nach Bedarf öffentlich sein
- Repos werden für das initiale Vercel-Deployment **vorübergehend öffentlich** gestellt und danach wieder auf intern gesetzt

## Branch-Strategie

### Standard: main / dev

Der Standardansatz bei allen WAMOCON-Apps:

```
main   ← Produktions-Branch, immer deploybar, kein direkter Commit
dev    ← Entwicklungs-Branch, aktive Arbeit
```

- Entwicklung geschieht auf `dev`
- PRs laufen von `dev` nach `main` nach Review und Tests
- Direkte Commits auf `main` sind nicht erlaubt

### Themenspezifisches Branching (vereinzelt)

Bei größeren Features oder paralleler Entwicklung können zusätzliche Branches genutzt werden:

```
feature/auth       ← Neues Feature
fix/bugname        ← Fehlerbehebung
hotfix/kritisch    ← Dringender Produktionsfehler
```

Diese Branches werden von `dev` abgezweigt und zurück nach `dev` gemergt.

**Grundregel:** Niemals direkt auf `main` commiten, immer über `dev` und dann PR.

## Naming Conventions

WAMOCON-Repositories verwenden zwei Schreibweisen:

- **`snake_case`** (kleingeschrieben, Wörter mit Unterstrich): z.B. `backup_planner`, `carman_lp`, `daily_echo`
- **`camelCase`** (Großbuchstabe am Wortanfang): z.B. `localSupabaseDB`, `AppMonitor`, `TeamRadar`

Sonderfälle und Ausnahmen sind im App-Katalog (Kapitel 9) dokumentiert.

## Repository-Struktur (Standard-App)

Alle App-Repos basieren auf dem `template_repo`-Template und haben diese Struktur:

```
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
```

## Secrets-Management

| Secret | Scope | Beschreibung |
| --- | --- | --- |
| `VERCEL_TOKEN` | Organisation | Vercel API-Token (org-weit konfiguriert) |
| `VERCEL_ORG_ID` | Organisation | Vercel Organisations-ID (org-weit konfiguriert) |
"""

JIRA = r"""# Kapitel 4 – Jira & Aufgabenmanagement

## Einsatz: Wann ist Jira verpflichtend?

| Projekttyp | Jira-Nutzung |
| --- | --- |
| **Wellen-Appentwicklung** (kleine, schnelle Apps im Wellen-Rhythmus) | **Optional** — empfohlen, aber nicht verpflichtend |
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
"""

SUPABASE_NEW_SECTIONS = {
    "email_fields": """**Angaben in der E-Mail:**

- App-Name (identisch mit dem GitHub-Repo-Namen)
""",
    "schemas": """### Empfohlene Schema-Struktur

| Schema | Zweck |
| --- | --- |
| `[appname]_dev` | Entwicklungs- und Testdaten (ersetzt `public`) |
| `[appname]_test` | Separates Test-Schema |
| `[appname]_prod` | Produktionsdaten (Trennung von Testdaten) |

Die Schema-Struktur ist empfohlen und kann projektspezifisch angepasst werden.
""",
    "migrations": """Schema-Änderungen können auf zwei Wegen vorgenommen werden:

**Option 1: Migrations-Dateien** (empfohlen, versionierbar)

**GitHub Copilot übernimmt die Erstellung und Ausführung der Migrationen** auf Basis des Anforderungsdokuments.

```bash
# Migration erstellen (Copilot generiert den SQL-Inhalt)
npx supabase migration new <migrations-name>
# Erstellt: supabase/migrations/<timestamp>_<name>.sql

# Migrationen lokal anwenden
npx supabase db reset

# Migrationen in Supabase Cloud anwenden
npx supabase db push

# Migrations-Status prüfen
npx supabase migration list
```

**Option 2: SQL Editor** (für schnelle Anpassungen)

Schema-Änderungen können auch direkt im SQL Editor des Supabase Dashboards vorgenommen werden.
In diesem Fall sollte die Änderung nachträglich als Migrations-Datei dokumentiert werden.

**Wichtig:** Migrations-Dateien in `supabase/migrations/` immer in Git committen. Bestehende Migrations-Dateien niemals nachträglich ändern.
"""
}

OEKOSYSTEM_INFRA_SECTION = """
## Infrastruktur-Repositories

Folgende Repositories sind keine Apps, sondern Infrastruktur-Komponenten der Organisation:

| Repository | Beschreibung |
| --- | --- |
| [github_workflow](https://github.com/Wamocon/github_workflow) | Zentrale CI/CD-Workflows der Organisation |
| [localSupabaseDB](https://github.com/Wamocon/localSupabaseDB) | Template für lokale Supabase-Instanzen |
| [template_repo](https://github.com/Wamocon/template_repo) | Basis-Template für alle neuen Apps |
"""

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Geschrieben: {os.path.relpath(path, BASE)}")

def fix_dashes(text):
    """Ersetzt Gedankenstriche (– und —) im Fließtext durch Kommas oder Punkte.
    Ausnahmen: Code-Blöcke, Tabellen-Trennzeichen, Pfeile."""
    lines = text.split('\n')
    result = []
    in_code = False
    for line in lines:
        # Toggle code block
        if re.match(r'^```', line):
            in_code = not in_code
        if in_code or line.startswith('    '):
            result.append(line)
            continue
        # Replace em-dash and en-dash used as parenthetical in prose
        # But keep → (arrow) and table separator | --- |
        line = re.sub(r'\s[–—]\s', ', ', line)
        result.append(line)
    return '\n'.join(result)

def fix_chapter_heading(text, old_num, new_num):
    """Tauscht die Kapitelnummer im H1-Heading aus."""
    return re.sub(
        rf'^# Kapitel {old_num} – ',
        f'# Kapitel {new_num} – ',
        text,
        count=1,
        flags=re.MULTILINE
    )

# ---------------------------------------------------------------------------
# Markdown-Dateien aktualisieren
# ---------------------------------------------------------------------------

def update_markdown_files():
    chapters = os.path.join(BASE, 'chapters')

    # 00 Einleitung
    path = os.path.join(chapters, '00_einleitung.md')
    write_file(path, EINLEITUNG)

    # 01 Quickstart (neu)
    path = os.path.join(chapters, '01_quickstart.md')
    write_file(path, QUICKSTART)

    # 06 GitHub
    path = os.path.join(chapters, '06_github-repository-struktur.md')
    content = fix_dashes(GITHUB)
    write_file(path, content)

    # 07 Tech Stack
    path = os.path.join(chapters, '07_tech-stack-standards.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '07', '2')
    # Soften mandatory language
    content = content.replace(
        'Dieser Standard gilt für alle neuen Apps und sollte nicht ohne Absprache abgewichen werden.',
        'Dieser Tech Stack ist der Standard für alle neuen Apps. Abweichungen sind möglich und können themenspezifisch begründet werden.'
    )
    # Fix dash in Server Components rule
    content = content.replace(
        '- **Server Components sind der Standard** — `"use client"` nur hinzufügen, wenn Interaktivität benötigt wird',
        '- **Server Components sind der Standard**, `"use client"` nur hinzufügen, wenn Interaktivität benötigt wird'
    )
    content = fix_dashes(content)
    write_file(path, content)

    # 08 Entwicklungsprozess
    path = os.path.join(chapters, '08_entwicklungsprozess.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '08', '3')
    # Fix blockquote dash
    content = content.replace(
        'Copilot ist nicht nur ein Hilfsmittel, sondern das primäre Entwicklungswerkzeug – von der Planung über die Implementierung bis hin zu Migrationen und Deployment-Konfigurationen.',
        'Copilot ist nicht nur ein Hilfsmittel, sondern das primäre Entwicklungswerkzeug, von der Planung über die Implementierung bis hin zu Migrationen und Deployment-Konfigurationen.'
    )
    # Fix flow chart step: "Template Repo klonen" → proper description
    content = content.replace(
        'Template Repo klonen → dev-Branch → Anforderungsdokument in Copilot laden',
        'Neues GitHub-Repository aus template_repo erstellen, dev-Branch anlegen, Anforderungsdokument in Copilot laden'
    )
    # Fix Strato email fields: remove Gedankenstriche
    content = content.replace(
        '- Kurzbeschreibung / Zweck der App\n- Gewünschte Region (z. B. `eu-central-1`)',
        ''
    )
    content = fix_dashes(content)
    write_file(path, content)

    # 09 Jira
    path = os.path.join(chapters, '09_jira-aufgabenmanagement.md')
    content = fix_dashes(JIRA)
    write_file(path, content)

    # 10 Supabase
    path = os.path.join(chapters, '10_supabase.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '10', '5')
    # Fix email fields: remove Kurzbeschreibung and Gewünschte Region
    content = content.replace(
        '- App-Name (identisch mit dem GitHub-Repo-Namen)\n- Kurzbeschreibung und Zweck der App\n- Gewünschte Region (z. B. `eu-central-1` für Deutschland)',
        '- App-Name (identisch mit dem GitHub-Repo-Namen)'
    )
    # Fix schemas
    content = content.replace(
        """### Empfohlene Schema-Struktur

| Schema | Zweck |
| --- | --- |
| `public` | Standard-Schema (Supabase-Default) |
| `test` | Entwicklungs- und Testdaten |
| `prod` | Produktionsdaten (Trennung von Testdaten) |""",
        """### Empfohlene Schema-Struktur

| Schema | Zweck |
| --- | --- |
| `[appname]_dev` | Entwicklungs- und Testdaten (ersetzt `public`) |
| `[appname]_test` | Separates Test-Schema |
| `[appname]_prod` | Produktionsdaten (Trennung von Testdaten) |

Die Schema-Struktur ist empfohlen und kann projektspezifisch angepasst werden."""
    )
    # Fix schema creation SQL to use new names
    content = content.replace(
        """```sql
CREATE SCHEMA IF NOT EXISTS test;
CREATE SCHEMA IF NOT EXISTS prod;

GRANT USAGE ON SCHEMA test TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA prod TO anon, authenticated, service_role;

GRANT ALL ON ALL TABLES IN SCHEMA test TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA test
  GRANT ALL ON TABLES TO anon, authenticated, service_role;

GRANT ALL ON ALL TABLES IN SCHEMA prod TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA prod
  GRANT ALL ON TABLES TO anon, authenticated, service_role;
```""",
        """```sql
-- Beispiel für App "carman"
CREATE SCHEMA IF NOT EXISTS carman_dev;
CREATE SCHEMA IF NOT EXISTS carman_test;
CREATE SCHEMA IF NOT EXISTS carman_prod;

GRANT USAGE ON SCHEMA carman_dev TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA carman_test TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA carman_prod TO anon, authenticated, service_role;

GRANT ALL ON ALL TABLES IN SCHEMA carman_dev TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA carman_test TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA carman_prod TO anon, authenticated, service_role;
```"""
    )
    # Add SQL Editor option to migrations section
    old_migrations = (
        'Schema-Änderungen werden **ausschließlich über Migrations-Dateien** vorgenommen — niemals direkt über das Supabase-Dashboard.\n\n'
        '**GitHub Copilot übernimmt die Erstellung und Ausführung der Migrationen** auf Basis des Anforderungsdokuments.'
    )
    new_migrations = (
        'Schema-Änderungen können auf zwei Wegen vorgenommen werden.\n\n'
        '**Option 1: Migrations-Dateien** (empfohlen, versionierbar)\n\n'
        '**GitHub Copilot übernimmt die Erstellung und Ausführung der Migrationen** auf Basis des Anforderungsdokuments.'
    )
    content = content.replace(old_migrations, new_migrations)
    # Add SQL Editor option after the migration commands block
    old_after_cmds = '**Wichtig:** Migrations-Dateien in `supabase/migrations/` immer in Git committen. Bestehende Migrations-Dateien niemals nachträglich ändern.'
    new_after_cmds = (
        '**Option 2: SQL Editor** (für schnelle Anpassungen)\n\n'
        'Schema-Änderungen können auch direkt im SQL Editor des Supabase Dashboards vorgenommen werden. '
        'In diesem Fall sollte die Änderung nachträglich als Migrations-Datei dokumentiert werden.\n\n'
        + old_after_cmds
    )
    content = content.replace(old_after_cmds, new_after_cmds)
    content = fix_dashes(content)
    write_file(path, content)

    # 11 Vercel
    path = os.path.join(chapters, '11_vercel-deployment.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '11', '6')
    content = fix_dashes(content)
    write_file(path, content)

    # 12 Sicherheit
    path = os.path.join(chapters, '12_sicherheit-code-qualitaet.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '12', '7')
    content = fix_dashes(content)
    write_file(path, content)

    # 13 KI
    path = os.path.join(chapters, '13_ki-entwicklung-copilot.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '13', '8')
    content = fix_dashes(content)
    write_file(path, content)

    # 14 Ökosystem
    path = os.path.join(chapters, '14_produkt-oekosystem.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '14', '9')
    # Remove infrastructure repos from App-Katalog
    for repo, desc in [
        ('github_workflow', 'Zentrale CI/CD-Workflows der Organisation'),
        ('localSupabaseDB', 'Template für lokale Supabase-Instanzen'),
        ('template_repo', 'Basis-Template für alle neuen Apps'),
    ]:
        content = re.sub(
            rf'\| \[{re.escape(repo)}\]\(https://github\.com/Wamocon/{re.escape(repo)}\) \| [^\n]+ \|\n',
            '',
            content
        )
    # Add Infrastruktur section before Landing Pages
    content = content.replace(
        '\n## Landing Page Repositories\n',
        OEKOSYSTEM_INFRA_SECTION + '\n## Landing Page Repositories\n'
    )
    content = fix_dashes(content)
    write_file(path, content)

    # 15 Glossar
    path = os.path.join(chapters, '15_glossar-referenzen.md')
    content = read_file(path)
    content = fix_chapter_heading(content, '15', '10')
    content = fix_dashes(content)
    write_file(path, content)

    print("Alle Markdown-Dateien aktualisiert.")

# ---------------------------------------------------------------------------
# HTML generieren
# ---------------------------------------------------------------------------

CHAPTERS = [
    ('kap00', 'chapters/00_einleitung.md'),
    ('kapQS', 'chapters/01_quickstart.md'),
    ('kap01', 'chapters/06_github-repository-struktur.md'),
    ('kap02', 'chapters/07_tech-stack-standards.md'),
    ('kap03', 'chapters/08_entwicklungsprozess.md'),
    ('kap04', 'chapters/09_jira-aufgabenmanagement.md'),
    ('kap05', 'chapters/10_supabase.md'),
    ('kap06', 'chapters/11_vercel-deployment.md'),
    ('kap07', 'chapters/12_sicherheit-code-qualitaet.md'),
    ('kap08', 'chapters/13_ki-entwicklung-copilot.md'),
    ('kap09', 'chapters/14_produkt-oekosystem.md'),
    ('kap10', 'chapters/15_glossar-referenzen.md'),
]

SIDEBAR_LABELS = [
    ('kap00', '00', 'Einleitung'),
    ('kapQS', 'QS', 'Quickstart'),
    ('kap01', '01', 'GitHub &amp; Repository-Struktur'),
    ('kap02', '02', 'Tech Stack &amp; Standards'),
    ('kap03', '03', 'Entwicklungsprozess'),
    ('kap04', '04', 'Jira &amp; Aufgabenmanagement'),
    ('kap05', '05', 'Supabase Cloud Projekt'),
    ('kap06', '06', 'Vercel Deployment'),
    ('kap07', '07', 'Sicherheit &amp; Code-Qualit\u00e4t'),
    ('kap08', '08', 'KI-Entwicklung &amp; Copilot-Workflows'),
    ('kap09', '09', 'Produkt-\u00d6kosystem &amp; App-Katalog'),
    ('kap10', '10', 'Glossar &amp; Referenzen'),
]

def preprocess_md(text):
    """Normalisiert schließende Fence-Marker (z.B. ```text → ```)."""
    lines = text.split('\n')
    result = []
    in_fence = False
    fence_char = '`'
    fence_len = 3
    for line in lines:
        if not in_fence:
            m = re.match(r'^(`{3,}|~{3,})', line)
            if m:
                fence_char = m.group(1)[0]
                fence_len = len(m.group(1))
                in_fence = True
                result.append(line)
            else:
                result.append(line)
        else:
            m = re.match(r'^([`~]+)', line)
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len:
                in_fence = False
                result.append(fence_char * fence_len)
            else:
                result.append(line)
    return '\n'.join(result)

def convert_md(text):
    text = preprocess_md(text)
    m = md_lib.Markdown(extensions=['tables', 'fenced_code'])
    return m.convert(text)

def build_html():
    index_path = os.path.join(BASE, 'index.html')
    html = read_file(index_path)

    # --- Sidebar ersetzen ---
    nav_items = '\n'.join(
        f'            <li><a href="#{kap_id}"><span class="kap-num">{num}</span> {label}</a></li>'
        for kap_id, num, label in SIDEBAR_LABELS
    )
    html = re.sub(
        r'(<nav>\s*<ol>).*?(</ol>\s*</nav>)',
        r'\1\n' + nav_items + r'\n          \2',
        html,
        count=1,
        flags=re.DOTALL
    )

    # --- Kapitel-Sections ersetzen ---
    # Alles zwischen erstem <section class="chapter" und letztem </section> (vor </main>)
    first = html.index('\n<section class="chapter"')
    # Find the last </section> before </main>
    last_section_end = html.rindex('</section>')
    last_section_end += len('</section>')

    sections_html = ''
    for kap_id, rel_path in CHAPTERS:
        md_path = os.path.join(BASE, rel_path)
        md_text = read_file(md_path)
        body = convert_md(md_text)
        sections_html += f'\n<section class="chapter" id="{kap_id}">\n{body}\n</section>\n'

    html = html[:first] + sections_html + html[last_section_end:]

    write_file(index_path, html)
    print("index.html regeneriert.")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("=== WAMOCON Entwicklerhandbuch Build ===")
    print("\n[1] Markdown-Dateien aktualisieren...")
    update_markdown_files()
    print("\n[2] HTML regenerieren...")
    build_html()
    print("\nFertig!")
