# Kapitel 2, Tech Stack & Standards

## Übersicht

Alle WAMOCON-Webanwendungen basieren auf einem einheitlichen Tech Stack.
Dieser Tech Stack ist der Standard für alle neuen Apps. Abweichungen sind möglich und können themenspezifisch begründet werden.

| Schicht | Technologie | Version |
| --- | --- | --- |
| Framework | Next.js (App Router) | 16.x |
| Sprache | TypeScript (strict mode) | 5.x |
| Styling | Tailwind CSS | v4 |
| Backend & Datenbank | Supabase (PostgreSQL, Auth, RLS) | 2.x |
| Deployment | Vercel |, |
| Package Manager | npm |, |
| Linter | ESLint | 9.x |
| Dev-Server | Next.js mit Turbopack |, |
| E2E-Tests | Playwright |, |

## Next.js 16, App Router

Alle Apps verwenden den **App Router** (`src/app/`). Der Pages Router wird nicht verwendet.

### Wichtigste Regeln

- **Server Components sind der Standard**, `"use client"` nur hinzufügen, wenn Interaktivität benötigt wird
- Server Actions in eigene Dateien auslagern (`actions.ts` im Feature-Ordner)
- `loading.tsx` und `error.tsx` für jedes Route-Segment anlegen
- Formulareingaben auf Client- und Server-Seite validieren
- `revalidatePath` / `revalidateTag` statt manuellem Cache-Busting verwenden
- `next/image` für alle Bilder verwenden (automatische Optimierung)
- `next/font` für Schriften verwenden (kein Layout-Shift)

### verfügbare npm-Scripts

| Befehl | Beschreibung |
| --- | --- |
| `npm run dev` | Dev-Server mit Turbopack starten (Hot Reload) |
| `npm run build` | Produktions-Build erstellen |
| `npm run start` | Produktionsserver starten |
| `npm run lint` | ESLint ausführen |
| `npm run typecheck` | TypeScript-Typprüfung ausführen |
| `npm run db:start` | Lokale Supabase-Instanz starten |
| `npm run db:stop` | Lokale Supabase-Instanz stoppen |
| `npm run db:reset` | Lokale Datenbank zurücksetzen |
| `npm run db:status` | Status der lokalen Supabase prüfen |

## TypeScript

Alle Projekte nutzen TypeScript im **Strict Mode** (`strict: true` in `tsconfig.json`).

### Konventionen

- **`any` vermeiden**, `unknown` verwenden und den Typ einschränken
- **Zod für Runtime-Validierung** an API-Grenzen einsetzen
- **Interfaces bevorzugen** gegenüber `type` für Objektformen (bessere Fehlermeldungen)
- **Typen zentral exportieren** pro Feature in `types.ts`
- Generierte Supabase-Typen verwenden:

```typescript
import { Database } from '@/types/supabase';
const supabase = createServerClient<Database>(...);
```text
## Tailwind CSS v4

Alle Apps verwenden Tailwind CSS v4 mit dem PostCSS-Plugin (`@tailwindcss/postcss`).

### Grundregeln

- Utility-First-Ansatz, keine separaten CSS-Dateien außer für globale Styles
- Responsive Design mit den Standard-Breakpoints von Tailwind
- Keine magischen Zahlen, Tailwind-Scale-Werte verwenden
- Das WAMOCON-Design-System (dunkler Blauverlauf, Akzentfarbe `#1fd0b0`) aus Kapitel 05 beachten

## Supabase

Supabase stellt PostgreSQL-Datenbank, Authentifizierung und Row Level Security bereit.
Details zur Konfiguration und Nutzung in **Kapitel 5, Supabase Cloud Projekt**.

### Supabase-Client-Regeln

- **`createServerClient`** in Server Components und Server Actions verwenden
- **`createBrowserClient`** nur in Client Components verwenden
- Fehler immer prüfen:

```typescript
const { data, error } = await supabase.from('users').select('*');
if (error) throw error;
```text
## Abhängigkeiten (Standard)

### Produktions-Dependencies

| Paket | Zweck |
| --- | --- |
| `next` | Framework |
| `react` / `react-dom` | UI-Library |
| `@supabase/supabase-js` | Supabase JavaScript Client |
| `@supabase/ssr` | Supabase SSR-Helpers für Next.js |
| `lucide-react` | Icon-Library |

### Entwicklungs-Dependencies

| Paket | Zweck |
| --- | --- |
| `typescript` | Sprachkompilierung |
| `eslint` | Linter |
| `eslint-config-next` | Next.js ESLint-Konfiguration |
| `tailwindcss` | CSS-Framework |
| `@tailwindcss/postcss` | Tailwind v4 PostCSS-Plugin |
| `@types/react` / `@types/node` | TypeScript-Typen |

## Umgebungsvariablen

Jedes Projekt hat eine `.env.example`-Datei als Template. Die eigentliche `.env.local` wird niemals in Git eingecheckt.

### Standard-Variablen

```env
# Next.js
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_SITE_NAME=<App-Name>

# Supabase (lokal)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<aus npx supabase status>
SUPABASE_SERVICE_ROLE_KEY=<aus npx supabase status>

# Supabase (Cloud)
# NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
# SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

# Schema
SUPABASE_DB_SCHEMA=public
```text
**Wichtig:** `NEXT_PUBLIC_`-Prefix bedeutet, dass die Variable im Browser sichtbar ist.
Der `SUPABASE_SERVICE_ROLE_KEY` darf **niemals** mit `NEXT_PUBLIC_` versehen werden.

## Globale Tools (Entwicklerrechner)

Jeder Entwickler sollte folgende Tools installiert haben:

```bash
# Node.js via nvm (Version 20)
nvm install 20
nvm use 20

# Vercel CLI
npm install -g vercel

# Supabase CLI
npm install -g supabase
```text
## VS Code Extensions (Empfohlen)

| Extension | Zweck |
| --- | --- |
| GitHub Copilot | KI-Code-Assistent |
| GitHub Copilot Chat | KI-Chat-Interface |
| ESLint | Linting |
| Prettier | Code-Formatierung |
| Tailwind CSS IntelliSense | Tailwind-Autovervollständigung |
| Error Lens | Inline-Fehleranzeige |
| GitLens | Git-Blame & History |
| Supabase | Supabase-Integration |

## VS Code Workspace-Einstellungen (Empfohlen)

In `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "files.exclude": {
    "**/.next": true,
    "**/node_modules": true
  }
}
```text
