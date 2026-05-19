# Kapitel 08 – Entwicklungsprozess

## Überblick: Von der Idee bis zur Produktion

```
Neue App anlegen
       │
       ▼
Template klonen & einrichten
       │
       ▼
Lokal entwickeln (Feature-Branches)
       │
       ▼
Lokal testen (typecheck → lint → dev-Server)
       │
       ▼
Pull Request erstellen
       │
       ├─→ CI: Auto-Fix (ESLint --fix, Formatierung)
       ├─→ CI: Checks (TypeScript + ESLint)
       └─→ Vercel: Preview-Deployment
                │
                ▼
          PR mergen → Vercel: Produktions-Deployment
```

## 1. Neue App anlegen

1. Im Browser: GitHub → `Wamocon/wamohub` → **Use this template** → **Create a new repository**
2. Repository in der `Wamocon`-Organisation anlegen, Name wählen
3. Sichtbarkeit: **Internal** (Standardeinstellung)

## 2. Repository klonen & einrichten

```bash
# Repository klonen
git clone https://github.com/Wamocon/<repo-name>.git
cd <repo-name>

# Abhängigkeiten installieren
npm install

# Umgebungsvariablen aus Template kopieren
cp .env.example .env.local
# .env.local mit Supabase-Credentials befüllen (siehe Kapitel 10)

# Entwicklungsserver starten
npm run dev
```

Die App läuft dann auf [http://localhost:3000](http://localhost:3000).

## 3. Workflow-Dateien aktualisieren

Nach dem Klonen: Workflow-Dateien in `.github/workflows/deploy.yml` und `.github/workflows/pr-pipeline.yml` öffnen und prüfen, dass `Wamocon/github_workflow` als Org/Repo-Referenz korrekt eingetragen ist.

## 4. Lokale Entwicklung

### Branch anlegen

```bash
# Ersten Stand auf main pushen (einmalig)
git add .
git commit -m "chore: initial setup"
git push origin main

# Ab jetzt: immer auf Feature-Branch arbeiten
git checkout -b feature/mein-feature
```

### Arbeitsloop

```bash
# Entwickeln und testen
npm run dev

# Vor jedem Commit prüfen
npm run typecheck   # TypeScript-Fehler finden
npm run lint        # Lint-Probleme finden

# Committen und pushen
git add .
git commit -m "feat: beschreibung der Änderung"
git push origin feature/mein-feature
```

### Wichtige Regeln

- **Lokal testen vor dem Push** — `typecheck` und `lint` müssen lokal grün sein
- **Alle Änderungen pushen, bevor der PR geöffnet wird** — jeder weitere Push auf einen offenen PR löst die gesamte CI-Pipeline aus (kostet GitHub-Actions-Minuten)
- **Nur einen offenen PR gleichzeitig** — erst mergen, dann neuen Branch anlegen

## 5. CI/CD-Pipeline (automatisch)

Die Pipeline läuft automatisch beim Öffnen eines PRs gegen `main`.

### PR-Pipeline

```
Push auf offenen PR
       │
       ├─→ pr-autofix: ESLint --fix, Prettier --write (committet automatisch zurück)
       │
       └─→ pr-checks:
               ├─ tsc --noEmit        (TypeScript)
               └─ eslint .            (Lint)
                      │
                      ├─ ❌ Fail → PR blockiert
                      └─ ✅ Pass → Vercel Preview-Deploy
```

### Deploy-Pipeline

| Auslöser | Ergebnis |
|---|---|
| Pull Request → `main` | Vercel **Preview**-Deployment (einzigartige URL pro PR) |
| Merge / Push → `main` | Vercel **Produktions**-Deployment |

## 6. Erstaliniges Vercel-Setup (einmalig pro App)

Da Vercel Zugriff auf den Repository-Code benötigt, gibt es bei internen Repos einen einmaligen Workaround:

1. **Repo vorübergehend öffentlich machen**: `Repository → Settings → General → Change visibility → Public`
2. Auf [vercel.com](https://vercel.com) → **Add New Project** → **Import** das Repo importieren
3. Projekt deployen
4. **Vercel Project ID kopieren**: `Vercel Project → Settings → General → Project ID`
5. **Als GitHub Secret hinzufügen**: `Repository → Settings → Secrets → Actions → New secret`
   - Name: `VERCEL_PROJECT_ID`
   - Wert: die kopierte Project ID
6. **Repo wieder auf intern setzen**: `Repository → Settings → General → Change visibility → Internal`
7. **Umgebungsvariablen in Vercel eintragen**: `Vercel Project → Settings → Environment Variables` → alle Variablen aus `.env.local` eintragen

> Die Org-weiten Secrets `VERCEL_TOKEN` und `VERCEL_ORG_ID` sind bereits auf Organisationsebene konfiguriert und müssen nicht manuell hinzugefügt werden.

## 7. Fehlerbehebung bei CI-Failures

### Vorgehen

1. **GitHub → Actions-Tab → Fehlgeschlagener Run öffnen**
2. Den fehlgeschlagenen Job-Schritt aufklappen → genaue Fehlermeldung lesen
3. Fehler lokal reproduzieren:

| Fehler | Lokale Reproduktion |
|---|---|
| TypeScript-Fehler | `npm run typecheck` |
| Lint-Fehler | `npm run lint` |
| Fehlende Abhängigkeiten | `package-lock.json` im Git prüfen |
| Vercel-Deploy schlägt fehl | Vercel-Secrets und Umgebungsvariablen prüfen |

### Häufige lokale Probleme

| Problem | Lösung |
|---|---|
| `Module not found` | `npm install` → Dev-Server neu starten |
| Veraltete Daten nach Migration | Dev-Server neu starten |
| TypeScript-Fehler in IDE, aber nicht im Terminal | `Ctrl+Shift+P` → „Restart TS Server" |
| `.env`-Änderungen werden nicht übernommen | `next dev` neu starten |
| Port bereits belegt | `npx kill-port 3000` |

## 8. Datenbank-Migrations-Workflow

Schema-Änderungen werden **immer versioniert** und niemals direkt über das Supabase-Dashboard gemacht.

```bash
# Neue Migration erstellen
npx supabase migration new <name>

# Migrationen anwenden (lokal)
npx supabase db reset

# Migrationen anwenden (Cloud via CLI)
npx supabase db push
```

Migrationen liegen in `supabase/migrations/` und werden mit Git versioniert.
Details in **Kapitel 10 – Supabase Cloud Projekt**.

## 9. Projekt-Checkliste für jede neue App

- [ ] Landing Page
- [ ] Handbuch / Manual (HOWTO.md)
- [ ] Hauptprozess (Kernfunktion der App)
- [ ] Demo-Video
- [ ] Domain (über Strato gesichert und in Vercel konfiguriert)
- [ ] Alle Env-Variablen in Vercel eingetragen
- [ ] RLS auf allen Supabase-Tabellen aktiviert
- [ ] Rechtliche Dokumente (Impressum, Datenschutzerklärung, AGB) aus `legal-docs/` angepasst

## 10. Schnellreferenz-Befehle

```bash
# Development
npm run dev

# Qualitätsprüfung
npm run typecheck
npm run lint

# Lint mit Auto-Fix
npx eslint . --fix

# Vercel
vercel link                 # Projekt verknüpfen
vercel env pull .env.local  # Env-Variablen ziehen
vercel deploy               # Preview-Deployment
vercel deploy --prod        # Produktions-Deployment

# Supabase
npx supabase migration new <name>   # Migration erstellen
npx supabase db push                # Migrationen anwenden
npx supabase db reset               # DB zurücksetzen (lokal)
```
