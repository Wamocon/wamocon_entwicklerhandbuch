# Kapitel 10 – Supabase Cloud Projekt

## Was ist Supabase?

WAMOCON nutzt **Supabase Pro** als primären Backend-as-a-Service für alle Apps. Es stellt bereit:

- **PostgreSQL-Datenbank** mit vollem SQL-Zugriff
- **Auth** — Benutzerauthentifizierung (E-Mail, OAuth, Magic Links)
- **Row Level Security (RLS)** — feingranulare Zugriffssteuerung auf Datenbankebene
- **Storage** — Dateispeicherung (Bilder, Dokumente)
- **Edge Functions** — Serverless-Funktionen (bei Bedarf)
- **REST & Realtime API** — automatisch generiert aus dem Datenbankschema

## 1. Beantragung (Pflicht vor Entwicklungsstart)

Das Supabase Cloud Projekt wird **per E-Mail beantragt** — kein Self-Service.

**Zeitpunkt:** Direkt nach Freigabe des Anforderungsdokuments (→ **Kapitel 08, Abschnitt 2**)

**Angaben in der E-Mail:**

- App-Name (identisch mit dem GitHub-Repo-Namen)
- Kurzbeschreibung und Zweck der App
- Gewünschte Region (z. B. `eu-central-1` für Deutschland)

> Durch frühzeitige Beantragung entsteht keine Wartezeit kurz vor dem Go-live.

## 2. Einrichtung (env.local)

Nach Projekterstellung im Supabase Dashboard folgende Credentials unter **Project Settings → API** abrufen und in `.env.local` eintragen:

```env
# Supabase Cloud
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxxx
SUPABASE_SERVICE_ROLE_KEY=xxxx
DATABASE_URL=postgresql://postgres:xxxx@db.xxxx.supabase.co:5432/postgres

# Schema (Standard: public)
SUPABASE_DB_SCHEMA=public
```text
| Variable | Quelle in Supabase | Verwendung |
| --- | --- | --- |
| `NEXT_PUBLIC_SUPABASE_URL` | Project Settings → API → Project URL | Verbindungsendpunkt |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Project Settings → API → anon public | Client-seitiger Zugriff (eingeschränkt) |
| `SUPABASE_SERVICE_ROLE_KEY` | Project Settings → API → service_role | Server-seitiger Vollzugriff |
| `DATABASE_URL` | Project Settings → Database → Connection string | Direkte Datenbankverbindung (CLI, MCP) |

> **Sicherheit:** `.env.local` niemals ins Repository committen (`.gitignore` prüfen).
> `SUPABASE_SERVICE_ROLE_KEY` **niemals** mit `NEXT_PUBLIC_`-Prefix versehen.

## 3. Schemas

### Empfohlene Schema-Struktur

| Schema | Zweck |
| --- | --- |
| `public` | Standard-Schema (Supabase-Default) |
| `test` | Entwicklungs- und Testdaten |
| `prod` | Produktionsdaten (Trennung von Testdaten) |

### Schema erstellen und Berechtigungen setzen

```sql
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
```text
Schemas über die API zugänglich machen: **Project Settings → API → Exposed schemas** → Schema-Namen hinzufügen.

## 4. Datenbankmigrationen

Schema-Änderungen werden **ausschließlich über Migrations-Dateien** vorgenommen — niemals direkt über das Supabase-Dashboard.

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
```text
**Wichtig:** Migrations-Dateien in `supabase/migrations/` immer in Git committen. Bestehende Migrations-Dateien niemals nachträglich ändern.

## 5. Row Level Security (RLS)

RLS muss für **jede Tabelle** aktiviert sein — Copilot wird mit der Anweisung gesteuert, RLS immer zu aktivieren und niemals deaktiviert zu lassen.

```sql
-- RLS aktivieren
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Nutzer sehen nur ihre eigenen Daten
CREATE POLICY "Eigene Daten lesen"
  ON public.profiles FOR SELECT
  USING (auth.uid() = user_id);
```text
RLS-Policies werden als Teil der Migrationen versioniert.

## 6. Supabase Auth

Auth-Konfiguration über das Supabase Dashboard:
- E-Mail / Passwort aktivieren/deaktivieren
- OAuth-Provider konfigurieren (Google, GitHub, etc.)
- E-Mail-Templates anpassen

In der App wird `@supabase/ssr` für serverseitige Auth-Integration genutzt (Details → **Kapitel 07 – Tech Stack**).

## 7. Lokale Supabase Instanz (Fallback & Entwicklungsphase)

### Wann nutzen?

- Supabase Cloud Projekt noch in Beantragung (→ Kapitel 08, Abschnitt 1)
- Offline-Entwicklung und schnelles Prototyping ohne Cloud-Anbindung

### Lokale Instanzen via localSupabaseDB

Das Repo [`Wamocon/localSupabaseDB`](https://github.com/Wamocon/localSupabaseDB) ermöglicht das parallele Hochfahren mehrerer lokaler Supabase-Instanzen für verschiedene App-Entwicklungen:

- Jede App bekommt eine eigene isolierte Instanz
- Setup gemäß der [README.md im localSupabaseDB-Repo](https://github.com/Wamocon/localSupabaseDB/blob/main/README.md)
- `.env.local` auf die lokale Instanz-URL zeigen lassen statt auf Supabase Cloud

```bash
# Lokale Instanz starten
npx supabase start

# Status und lokale Credentials anzeigen
npx supabase status
```text
Lokale Credentials in `.env.local` eintragen:

```env
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<aus npx supabase status>
SUPABASE_SERVICE_ROLE_KEY=<aus npx supabase status>
```text
### ⚠️ Hardware-Limit: Huawei-Laptop RAM

Bei mehr als **2 parallelen lokalen Supabase-Instanzen** und **2 gleichzeitig laufenden Apps** stößt der Huawei-Laptop an seine RAM-Grenzen.

Symptome: Verlangsamte Response-Zeiten, App-Freezes, Instanz-Abstürze.

**Empfehlung:** Maximal 2 lokale Supabase-Instanzen + 2 aktive Apps gleichzeitig betreiben. Nicht benötigte Instanzen aktiv stoppen.

### Wechsel lokal → Supabase Cloud

Sobald das Supabase Cloud Projekt genehmigt ist:

1. `.env.local` Variablen auf die Cloud-Werte aktualisieren
2. Lokal entwickelte Migrationen in Supabase Cloud anwenden: `npx supabase db push`
3. Lokale Instanz stoppen: `npx supabase stop`
4. Ressourcen freigeben

## 8. Supabase MCP für GitHub Copilot

Der Supabase MCP (Model Context Protocol) Server gibt Copilot Zugriff auf das echte Datenbankschema.

Details zur Konfiguration → **Kapitel 13 – KI-Entwicklung & Copilot-Workflows**

## 9. Checkliste: Supabase-Setup

- [ ] Supabase Cloud Projekt per E-Mail beantragt (direkt nach Anforderungsfreigabe)
- [ ] Projekt erstellt und Status „Healthy"
- [ ] `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL` in `.env.local` eingetragen
- [ ] Alle Variablen als Vercel Environment Variables hinterlegt (→ Kapitel 11)
- [ ] `SUPABASE_SERVICE_ROLE_KEY` **kein** `NEXT_PUBLIC_`-Prefix
- [ ] `.env.local` in `.gitignore` vorhanden
- [ ] RLS für alle Tabellen aktiviert
- [ ] Erste Migration erstellt und in `supabase/migrations/` committed
- [ ] MCP für lokale Copilot-Tools konfiguriert (→ Kapitel 13)
