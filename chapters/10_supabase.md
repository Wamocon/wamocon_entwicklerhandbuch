# Kapitel 10 – Supabase Cloud Projekt

## Was ist Supabase?

Supabase ist der Backend-as-a-Service für alle WAMOCON-Apps. Es stellt bereit:

- **PostgreSQL-Datenbank** mit vollem SQL-Zugriff
- **Auth** — Benutzerauthentifizierung (E-Mail, OAuth)
- **Row Level Security (RLS)** — feingranulare Zugriffssteuerung auf Datenbankebene
- **Storage** — Dateispeicherung
- **Edge Functions** — Serverless-Funktionen (bei Bedarf)
- **REST & Realtime API** — automatisch generiert aus dem Datenbankschema

## 1. Neues Cloud-Projekt anlegen

1. Gehe zu [supabase.com/dashboard](https://supabase.com/dashboard)
2. **New project** klicken
3. Organisation auswählen
4. Projektname setzen (identisch mit dem GitHub-Repository-Namen)
5. Datenbankpasswort und Region setzen
6. Projekt erstellen — Status abwarten bis „Healthy"

## 2. Credentials sammeln

Nach der Erstellung im Dashboard unter **Project Settings → API**:

| Variable | Quelle | Zweck |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Project URL | Verbindungsendpunkt |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon public key | Clientseitiger, eingeschränkter Zugriff |
| `SUPABASE_SERVICE_ROLE_KEY` | service_role key | Serverseitiger Vollzugriff (niemals im Browser!) |

Diese Werte in `.env.local` eintragen und in Vercel als Environment Variables hinterlegen.

## 3. Schemas

Standardmäßig ist nur das `public`-Schema über die Supabase-API erreichbar.

### Empfohlene Schema-Struktur

| Schema | Zweck |
|---|---|
| `public` | Standard-Schema (Supabase-Default) |
| `test` | Daten für Entwicklung und Tests |
| `prod` | Produktionsdaten (Trennung von Testdaten) |

### Schema erstellen und Berechtigungen setzen

```sql
CREATE SCHEMA IF NOT EXISTS test;
CREATE SCHEMA IF NOT EXISTS prod;

-- Berechtigungen für Supabase-Rollen vergeben
GRANT USAGE ON SCHEMA test TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA prod TO anon, authenticated, service_role;

GRANT ALL ON ALL TABLES IN SCHEMA test TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA test
  GRANT ALL ON TABLES TO anon, authenticated, service_role;

GRANT ALL ON ALL TABLES IN SCHEMA prod TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA prod
  GRANT ALL ON TABLES TO anon, authenticated, service_role;
```

Schema über die Supabase-API zugänglich machen: **Project Settings → API → Exposed schemas** → Schema-Namen hinzufügen.

> Ohne diese Berechtigungen gibt PostgREST leere Ergebnisse oder Fehler zurück.

## 4. Migrations-Workflow

Schema-Änderungen werden **ausschließlich über Migrations-Dateien** vorgenommen — nie direkt über das Supabase-Dashboard-UI.

### Migration erstellen

```bash
npx supabase migration new <migrations-name>
# Erstellt: supabase/migrations/<timestamp>_<name>.sql
```

### Migration bearbeiten

Die erstellte SQL-Datei in `supabase/migrations/` öffnen und die Datenbankänderungen eintragen.

### Migration anwenden

```bash
# Lokal (Docker läuft)
npx supabase db reset

# Cloud
npx supabase db push
```

### Migrations-Status prüfen

```bash
npx supabase migration list
```

**Wichtige Regeln:**

- Migrations-Dateien werden mit Git versioniert — immer committen
- Bestehende Migrations-Dateien niemals nachträglich ändern — neue Migration erstellen
- Testdaten nicht als lokale Fixture-Dateien ablegen — direkt in Supabase eintragen

## 5. Row Level Security (RLS)

RLS ist für **alle Tabellen verpflichtend**. Ohne RLS hat jeder authentifizierte Nutzer vollen Tabellenzugriff.

### RLS aktivieren und Policy erstellen (Beispiel)

```sql
-- RLS aktivieren
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Nutzer sehen nur ihr eigenes Profil
CREATE POLICY "Users can view own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Nutzer können ihr Profil bearbeiten
CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = user_id);
```

## 6. Supabase-Client in Next.js

### Server Components / Server Actions

```typescript
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

const supabase = createServerClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  { cookies: () => cookies() }
);
```

### Client Components

```typescript
import { createBrowserClient } from '@supabase/ssr';

const supabase = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

### Fehlerbehandlung (immer prüfen!)

```typescript
const { data, error } = await supabase.from('users').select('*');
if (error) throw error;
```

## 7. Lokale Entwicklung mit localSupabaseDB

Wenn noch kein Supabase-Cloud-Projekt existiert, kann lokal mit dem `localSupabaseDB`-Template gearbeitet werden.

### Voraussetzungen

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) läuft

### Einrichtung

```bash
# localSupabaseDB als eigenes Repo klonen (Template verwenden)
git clone https://github.com/Wamocon/localSupabaseDB.git
cd localSupabaseDB

npm install
```

### Lokale Instanz starten

```bash
# Im App-Verzeichnis
npm run db:start
# oder direkt:
npx supabase start
```

Nach dem Start zeigt Supabase die lokalen Credentials an. Diese in `.env.local` eintragen:

```env
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<aus npx supabase status>
SUPABASE_SERVICE_ROLE_KEY=<aus npx supabase status>
```

### Hardware-Hinweis

Bei mehr als zwei parallelen lokalen Supabase-Instanzen und zwei laufenden Apps stößt Hardware mit wenig RAM (z. B. Huawei-Geräte) an Grenzen.
**Empfehlung:** Maximal zwei lokale Instanzen plus zwei aktive Apps gleichzeitig betreiben.

Sobald das Cloud-Projekt verfügbar ist, auf Supabase Cloud umstellen und lokale Ressourcen freigeben.

## 8. Supabase MCP für KI-Assistenten

Das Supabase MCP (Model Context Protocol) ermöglicht es GitHub Copilot, den echten Datenbankschema-Kontext zu lesen. Dadurch generiert Copilot akkuraten Code statt zu raten.

Details dazu in **Kapitel 13 – KI-Entwicklung & Copilot-Workflows**.

## 9. Checkliste: Supabase-Integration

- [ ] Cloud-Projekt erstellt und Status „Healthy"
- [ ] URL und Keys in `.env.local` eingetragen
- [ ] URL und Keys als Vercel Environment Variables konfiguriert
- [ ] `test`- und `prod`-Schemas erstellt (falls verwendet)
- [ ] Schema-Grants vergeben und Schemas in API Exposed Schemas eingetragen
- [ ] RLS für alle Tabellen aktiviert
- [ ] Erste Migration erstellt und committed
- [ ] MCP für lokale KI-Tools konfiguriert
- [ ] `SUPABASE_SERVICE_ROLE_KEY` nur server-seitig genutzt (kein `NEXT_PUBLIC_`-Prefix)
