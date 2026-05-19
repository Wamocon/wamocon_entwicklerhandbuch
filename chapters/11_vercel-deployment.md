# Kapitel 11 – Vercel Deployment

## Überblick

Alle WAMOCON-Apps werden über **Vercel** deployed. Das Deployment wird vollständig über GitHub Actions automatisiert — es muss kein manueller `vercel`-Befehl ausgeführt werden (außer beim initialen Setup).

## Deployment-Typen

| Auslöser | Deployment-Typ | Ergebnis |
|---|---|---|
| Pull Request gegen `main` | **Preview** | Einzigartige URL pro PR (z. B. `app-abc123.vercel.app`) |
| Merge / Push auf `main` | **Produktion** | Live unter der konfigurierten Domain |

## Zentraler CI/CD-Workflow

Das Deployment nutzt die wiederverwendbaren Workflows aus `Wamocon/github_workflow`:

```
PR öffnen
  └─→ pr-autofix.yml   → Lint-Fehler automatisch committen
  └─→ pr-checks.yml    → TypeScript + ESLint validieren
  └─→ deploy-preview.yml → Vercel Preview deployen

PR auf main mergen
  └─→ deploy-production.yml → Vercel Produktion deployen
```

## Erforderliche Secrets & Variablen

### GitHub-Organisationsebene (bereits konfiguriert)

| Secret | Beschreibung |
|---|---|
| `VERCEL_TOKEN` | Vercel API-Token der Organisation |
| `VERCEL_ORG_ID` | Vercel Organisations-ID |

Diese Secrets sind org-weit gesetzt und müssen nicht pro Repo konfiguriert werden.

### GitHub-Repository-Ebene (pro Repo einmalig)

| Secret | Beschreibung | Quelle |
|---|---|---|
| `VERCEL_PROJECT_ID` | Vercel-Projekt-ID der App | Vercel → Project Settings → General → Project ID |

## Erstmaliges Setup (einmalig pro App)

Da Vercel bei internen GitHub-Repos keinen direkten Lesezugriff hat, ist ein einmaliger Workaround notwendig:

### Schritt-für-Schritt

1. **Repo temporär öffentlich machen**
   - `Repository → Settings → General → Change visibility → Public`

2. **Vercel-Projekt importieren**
   - [vercel.com](https://vercel.com) → **Add New Project** → **Import** das Repo auswählen
   - Framework wird automatisch erkannt (Next.js)
   - Erstes Deployment durchführen

3. **Vercel Project ID kopieren**
   - `Vercel Project → Settings → General → Project ID`
   - Den Wert kopieren

4. **GitHub Secret anlegen**
   - `Repository → Settings → Secrets and variables → Actions → New repository secret`
   - Name: `VERCEL_PROJECT_ID`
   - Wert: die kopierte Project ID

5. **Repo auf intern zurücksetzen**
   - `Repository → Settings → General → Change visibility → Internal`

6. **Umgebungsvariablen in Vercel eintragen**
   - `Vercel Project → Settings → Environment Variables`
   - Alle Variablen aus `.env.local` eintragen

> **Wichtig:** Ohne die Umgebungsvariablen in Vercel schlägt jeder Build fehl.

## Umgebungsvariablen in Vercel

Für jede Variable den korrekten Scope setzen:

| Scope | Verwendung |
|---|---|
| **Production** | Live-Deployment (main-Branch) |
| **Preview** | PR-Deployments |
| **Development** | `vercel env pull` für lokale Entwicklung |

Üblicherweise gelten Supabase-Variablen für Production und Preview (ggf. mit unterschiedlichen Werten für `test`- vs. `prod`-Schema).

## Domain-Verwaltung

1. Domain bei [Strato](https://www.strato.de) erwerben
2. In Vercel: `Project → Settings → Domains → Add`
3. DNS-Einträge bei Strato konfigurieren (wie von Vercel angegeben):
   - **A-Record**: für Root-Domain (`@`)
   - **CNAME-Record**: für Subdomain (`www`)
4. Zertifikat wird von Vercel automatisch ausgestellt (Let's Encrypt)

## Vercel-spezifische Next.js-Einstellungen

In `next.config.ts`:

```typescript
const nextConfig = {
  // Strenge Typprüfung während Build
  typescript: {
    ignoreBuildErrors: false,
  },
  // ESLint während Build
  eslint: {
    ignoreDuringBuilds: false,
  },
};

export default nextConfig;
```

## Fehlerbehebung bei Deployment-Failures

### Häufige Fehlerquellen

| Problem | Lösung |
|---|---|
| Build schlägt mit TypeScript-Fehler fehl | `npm run typecheck` lokal ausführen und Fehler beheben |
| Build schlägt mit Lint-Fehler fehl | `npm run lint` lokal ausführen |
| Fehlende Umgebungsvariable im Build | In Vercel → Environment Variables prüfen |
| Supabase-Verbindung schlägt fehl | Supabase-URL und Keys in Vercel-Variables prüfen |
| Deployment läuft nicht an | `VERCEL_PROJECT_ID` Secret und Workflow-Referenz prüfen |

### Deployment-Logs einsehen

- **Vercel Dashboard** → Project → Deployments → jeweiliges Deployment öffnen
- **GitHub Actions** → Actions-Tab → Workflow-Run öffnen

## Vercel CLI Kurzreferenz

```bash
# Vercel-Projekt verknüpfen (einmalig)
vercel link

# Env-Variablen aus Vercel lokal ziehen
vercel env pull .env.local

# Manuelles Preview-Deployment (normalerweise nicht nötig)
vercel deploy

# Manuelles Produktions-Deployment (normalerweise nicht nötig)
vercel deploy --prod
```

## Checkliste: Vercel-Setup

- [ ] Repo temporär öffentlich gemacht
- [ ] Vercel-Projekt importiert und erstmals deployed
- [ ] `VERCEL_PROJECT_ID` als GitHub Repository Secret eingetragen
- [ ] Repo auf intern zurückgesetzt
- [ ] Alle `.env.local`-Variablen in Vercel Environment Variables eingetragen
- [ ] Scopes (Production/Preview/Development) für alle Variablen korrekt gesetzt
- [ ] Domain in Vercel hinzugefügt
- [ ] DNS bei Strato konfiguriert
- [ ] Automatischer Deploy nach Merge auf `main` getestet
