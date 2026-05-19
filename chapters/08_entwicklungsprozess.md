# Kapitel 08 – Entwicklungsprozess

> **Wichtig:** Die gesamte App-Entwicklung bei WAMOCON wird vollständig mit **GitHub Copilot** durchgeführt. Copilot ist nicht nur ein Hilfsmittel, sondern das primäre Entwicklungswerkzeug – von der Planung über die Implementierung bis hin zu Migrationen und Deployment-Konfigurationen.

## Überblick: Von der Idee bis zur Produktion

```text
Produktidee & Anforderungserstellung (manuell)
       │
       ▼
Anforderungsdokument in OneDrive ablegen & einreichen
       │
       ▼
Freigabe abwarten
       │
       ├─→ Supabase Cloud Projekt per E-Mail beantragen (→ Kapitel 10)
       └─→ Strato-Domain per E-Mail beantragen (→ Kapitel 11)
                │
                ▼
Template Repo klonen → dev-Branch → Anforderungsdokument in Copilot laden
       │
       ▼
Copilot erstellt Entwicklungsplan → iterative Implementierung
       │
       ▼
Lokale Tests → PR dev → main → Vercel Produktion
       │
       ▼
Landing Page generieren (bevorzugt GitHub Pages, optional Vercel)
```text
---

## 1. Produktidee & Anforderungserstellung

Die Ideenfindung und erste Anforderungsdefinition erfolgen **manuell durch den Entwickler**.

### Anforderungsdokument erstellen

**Bevorzugter Weg:** Das **[WMC-Anforderungsportal](https://github.com/Wamocon/WMC-Anforderungsportal)** nutzen.

**Alternativer Weg:** Anforderungsdokument manuell erstellen und per E-Mail einreichen.

Das Anforderungsdokument enthält:
- App-Name und Kurzbeschreibung
- Zielgruppe und Hauptnutzen
- Kernfunktionen und Anforderungen
- Gewünschtes Datenbankschema (grob)
- Technische Rahmenbedingungen

### Ablage in OneDrive

Das fertige Anforderungsdokument wird in **OneDrive** abgelegt:

```text
OneDrive / Welle [Nummer] / [App-Name] / Anforderungsdokument_[App-Name].docx
```text
**Wichtig:** Die Entwicklung beginnt **erst nach Freigabe** des Anforderungsdokuments.

---

## 2. Nach Freigabe: Infrastruktur beantragen

Direkt nach der Freigabe des Anforderungsdokuments — damit keine Wartezeit beim Go-live entsteht:

### Supabase Cloud Projekt beantragen

Das Supabase Cloud Projekt wird **per E-Mail beantragt** (kein Self-Service).

Angaben in der E-Mail:
- App-Name (identisch mit dem geplanten Repo-Namen)
- Kurzbeschreibung / Zweck der App
- Gewünschte Region (z. B. `eu-central-1`)

Details zur Einrichtung nach Freigabe → **Kapitel 10 – Supabase Cloud Projekt**

### Strato-Domain beantragen

Die Domain für die App wird **per E-Mail bei Strato beantragt**.

- Domain-Name angeben (z. B. `app-name.de` oder `app-name.wamocon.de`)
- Nach Zuteilung wird die Domain in Vercel konfiguriert → **Kapitel 11 – Vercel Deployment**

---

## 3. Entwicklungsstart: Template Repo & GitHub Copilot

### Repository anlegen

1. Auf GitHub: [`Wamocon/template_repo`](https://github.com/Wamocon/template_repo) → **„Use this template"** → **„Create a new repository"**
2. Repository in der `Wamocon`-Organisation anlegen
3. Name nach Naming Convention setzen (→ **Kapitel 06**)
4. Sichtbarkeit: **Internal**
5. `dev`-Branch anlegen — `main` bleibt geschützt

### Anforderungsdokument in GitHub Copilot laden

Das freigegebene Anforderungsdokument als Kontext in GitHub Copilot laden und Copilot anweisen, einen vollständigen Entwicklungsplan zu erstellen:

```text
Lade das Anforderungsdokument aus OneDrive und erstelle auf Basis dieses Dokuments
einen vollständigen Entwicklungsplan für die App [App-Name]:

- Datenbankschema & Migrationen (Tabellen, Spalten, RLS-Policies)
- Komponentenstruktur (Seiten, UI-Komponenten, Layouts)
- API-Endpunkte und Server Actions
- Meilensteine & Aufgabenpakete in sinnvoller Reihenfolge
```text
### Entwicklung mit Copilot durchführen

Copilot übernimmt:
- Datenbankmigrationen erstellen und ausführen
- Komponenten und Seiten implementieren
- API-Routen und Server Actions schreiben
- Konfigurationsdateien anpassen
- Deployment-Workflows konfigurieren

**Entwickler-Rolle:** Anforderungen definieren, Copilot steuern, Output reviewen und freigeben.

Die Entwicklung läuft **iterativ entlang des Copilot-Plans**:
1. Plan-Schritt lesen
2. Copilot anweisen diesen Schritt umzusetzen
3. Output lokal testen
4. Bei Problemen: Copilot korrigieren
5. Nächsten Schritt

---

## 4. Lokale Entwicklung & Datenbankmigrationen

### Umgebung einrichten

```bash
# Repository klonen
git clone https://github.com/Wamocon/<repo-name>.git
cd <repo-name>

# Auf dev-Branch wechseln
git checkout dev

# Abhängigkeiten installieren
npm install

# Umgebungsvariablen einrichten
cp .env.example .env.local
# Supabase-Credentials in .env.local eintragen (→ Kapitel 10)

# Entwicklungsserver starten
npm run dev
```text
### Supabase-Fallback: Lokale Instanz

Solange das Supabase Cloud Projekt noch **in Beantragung** ist, lokale Instanz nutzen:
→ **Kapitel 10.5 – Lokale Supabase Instanz**

### Datenbankmigrationen

GitHub Copilot erstellt und führt Migrationen direkt aus der App heraus in Supabase Cloud durch:

```bash
# Migration erstellen (Copilot generiert den SQL-Inhalt)
npx supabase migration new <migrations-name>

# Migration lokal anwenden (Fallback auf lokaler Instanz)
npx supabase db reset

# Migration in Supabase Cloud anwenden
npx supabase db push
```text
Migrationshistorie wird im Repo unter `/supabase/migrations/` versioniert.

### Lokale Qualitätsprüfung vor Commit

```bash
npm run typecheck   # TypeScript-Fehler
npm run lint        # Lint-Probleme
npm run dev         # Manuell testen
```text
---

## 5. CI/CD-Pipeline (automatisch)

### Bei Push auf `dev`: Preview-Deployment

```text
Push auf dev
  └─→ pr-autofix: ESLint --fix (committet zurück)
  └─→ pr-checks: TypeScript + ESLint validieren
  └─→ Vercel: Preview-Deployment
```text
### Bei Merge auf `main`: Produktions-Deployment

```text
PR von dev → main gemergt
  └─→ Vercel: Produktions-Deployment
```text
Details → **Kapitel 11 – Vercel Deployment**

---

## 6. Landing Page generieren

Jede App bekommt ein eigenes Landing-Page-Repository: `[app-name]_lp`

Landing Pages werden **nicht manuell gebaut**, sondern über den **KI-Generierungs-Workflow** erstellt:

### Prozess

1. App-Beschreibung und Key Features als Prompt aufbereiten
2. KI-Workflow triggern (GitHub Actions / n8n-basiert)
3. KI generiert vollständige HTML-Landing-Page
4. Entwickler reviewed Output und mergt nach `main`
5. Automatisches Deployment

### Deployment

- **Bevorzugt:** GitHub Pages (kostenlos, kein Build-Step, direkt über GitHub)
- **Optional:** Vercel (für erweiterte Deployment-Features)

Standard: reines HTML, kein Framework-Overhead — direkt deploybar ohne Build-Prozess.

---

## 7. Schnellreferenz-Befehle

```bash
# Development
npm run dev
npm run typecheck
npm run lint

# Supabase
npx supabase migration new <name>   # Migration erstellen
npx supabase db push                # In Supabase Cloud deployen
npx supabase db reset               # Lokal zurücksetzen

# Git-Workflow
git checkout dev                    # Auf dev-Branch
git checkout -b feature/xyz         # Themenspezifischer Branch (von dev)
git push origin dev                 # Auf dev pushen → Preview Deploy
```text
