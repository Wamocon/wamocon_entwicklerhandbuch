# Kapitel 6, Vercel Deployment

## Überblick

Alle WAMOCON-TypeScript-Apps werden über **Vercel** deployed. WAMOCON nutzt den **Vercel Hobby Plan**. Das Deployment ist vollständig über den GitHub Actions Workflow aus dem [`template_repo`](https://github.com/Wamocon/template_repo) automatisiert.

**Landing Pages** werden bevorzugt über **GitHub Pages** veröffentlicht (Vercel ist optional).

## Deployment-Typen

| Auslöser | Deployment-Typ | Ergebnis |
| --- | --- | --- |
| Push auf `dev`-Branch | **Preview** | Einzigartige Preview-URL pro Branch |
| Merge / Push auf `main` | **Produktion** | Live unter der konfigurierten Domain |

## Zentraler CI/CD-Workflow

Aus dem [`Wamocon/github_workflow`](https://github.com/Wamocon/github_workflow) Repository:

```text
Push auf dev
  └─→ pr-autofix.yml   → Lint-Fehler automatisch committen
  └─→ pr-checks.yml    → TypeScript + ESLint validieren
  └─→ deploy-preview.yml → Vercel Preview deployen

Merge auf main
  └─→ deploy-production.yml → Vercel Produktions-Deploy
```text
## Erforderliche Secrets & Variablen

### GitHub-Organisationsebene (bereits konfiguriert, nichts zu tun)

| Secret | Beschreibung |
| --- | --- |
| `VERCEL_TOKEN` | Vercel API-Token der Organisation |
| `VERCEL_ORG_ID` | Vercel Organisations-ID |

### GitHub-Repository-Ebene (einmalig pro App)

| Secret | Beschreibung | Quelle |
| --- | --- | --- |
| `VERCEL_PROJECT_ID` | Vercel-Projekt-ID der App | Vercel → Project Settings → General → Project ID |

## Erstmaliges Setup (einmalig pro App)

Da Vercel bei internen GitHub-Repos keinen direkten Lesezugriff hat, ist folgender einmaliger Workaround notwendig:

### Schritt-für-Schritt

1. **Repo temporär öffentlich machen**
   - `Repository → Settings → General → Change visibility → Public`

2. **Vercel-Projekt importieren**
   - [vercel.com](https://vercel.com) → **Add New Project** → **Import** → Repo auswählen
   - Framework wird automatisch erkannt (Next.js)
   - Erstes Deployment durchführen

3. **Vercel Project ID kopieren**
   - `Vercel Project → Settings → General → Project ID`

4. **GitHub Secret anlegen**
   - `Repository → Settings → Secrets and variables → Actions → New repository secret`
   - Name: `VERCEL_PROJECT_ID`
   - Wert: die kopierte Project ID

5. **Repo auf intern zurücksetzen**
   - `Repository → Settings → General → Change visibility → Internal`

6. **Umgebungsvariablen in Vercel eintragen**
   - `Vercel Project → Settings → Environment Variables`
   - Alle Variablen aus `.env.local` eintragen (Supabase URL, Keys etc.)

> **Wichtig:** Ohne die Umgebungsvariablen schlägt jeder Build fehl.

## Umgebungsvariablen in Vercel

Für jede Variable den korrekten Scope setzen:

| Scope | Verwendung |
| --- | --- |
| **Production** | Live-Deployment (main-Branch) |
| **Preview** | Dev-Branch-Deployments |
| **Development** | `vercel env pull` für lokale Entwicklung |

## Domain-Verwaltung

1. Domain bei [Strato](https://www.strato.de) per E-Mail beantragen (→ **Kapitel 3, Abschnitt 2**)
2. In Vercel: `Project → Settings → Domains → Add`
3. DNS-Einträge bei Strato konfigurieren:
   - **A-Record** für Root-Domain (`@`)
   - **CNAME-Record** für Subdomain (`www`)
4. SSL-Zertifikat wird von Vercel automatisch ausgestellt (Let's Encrypt)

## Landing Pages: GitHub Pages (bevorzugt) vs. Vercel

Landing Pages (`[app-name]_lp`) werden bevorzugt über **GitHub Pages** veröffentlicht:

### GitHub Pages Setup für Landing Pages

1. Im Repo: `Settings → Pages → Source: Deploy from a branch`
2. Branch: `main`, Verzeichnis: `/ (root)` oder `/docs`
3. GitHub Pages URL: `https://wamocon.github.io/[repo-name]/`

**Vorteile GitHub Pages:**
- Kostenlos, kein Build-Step nötig
- Reines HTML, direkt deploybar
- Kein Vercel-Projekt nötig

**Optional Vercel:** Wenn erweiterte Deployment-Features oder Custom Domain mit SSL-Handling über Vercel gewünscht sind.

## Hobby Plan: Limits & Besonderheiten

| Limit | Wert |
| --- | --- |
| Bandbreite pro Monat | 100 GB |
| Serverless Functions | 100.000 Invocations/Monat |
| Team-Sharing | Nicht ohne Upgrade möglich |
| Deploy-Dauer | Max. 45 Minuten |

Bei Annäherung an Limits: Koordination mit dem Verantwortlichen für den Vercel-Account.

## Fehlerbehebung bei Deployment-Failures

| Problem | Lösung |
| --- | --- |
| TypeScript-Fehler im Build | `npm run typecheck` lokal ausführen |
| Lint-Fehler im Build | `npm run lint` lokal ausführen |
| Fehlende Umgebungsvariable | Vercel → Environment Variables prüfen |
| Supabase-Verbindungsfehler | Supabase-URL und Keys in Vercel prüfen |
| Deploy startet nicht | `VERCEL_PROJECT_ID` Secret und Workflow-Referenz prüfen |

## Checkliste: Vercel-Setup

- [ ] Repo temporär öffentlich gemacht für initialen Import
- [ ] Vercel-Projekt importiert und erstmals deployed
- [ ] `VERCEL_PROJECT_ID` als GitHub Repository Secret eingetragen
- [ ] Repo auf intern zurückgesetzt
- [ ] Alle `.env.local`-Variablen in Vercel Environment Variables eingetragen
- [ ] Scopes (Production/Preview/Development) für alle Variablen gesetzt
- [ ] Domain in Vercel hinzugefügt (nach Strato-Beantragung)
- [ ] DNS bei Strato konfiguriert
- [ ] Automatischer Deploy nach Merge auf `main` getestet
