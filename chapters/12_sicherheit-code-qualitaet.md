# Kapitel 12 – Sicherheit & Code-Qualität

## Grundsätze

Sicherheit wird nicht nachträglich ergänzt, sondern von Anfang an eingebaut. Jede neue App muss die folgenden Mindeststandards erfüllen, bevor sie in Produktion geht.

## Supabase-Sicherheit

### Row Level Security (RLS) — Pflicht

RLS muss für **jede Tabelle** aktiviert sein. Ohne RLS hat jeder authentifizierte Nutzer uneingeschränkten Zugriff.

```sql
-- RLS aktivieren
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Nutzer sehen nur ihre eigenen Daten
CREATE POLICY "Eigene Daten lesen"
  ON public.profiles FOR SELECT
  USING (auth.uid() = user_id);
```text
### Service Role Key

- `SUPABASE_SERVICE_ROLE_KEY` **niemals** im Browser-Code verwenden
- Niemals mit `NEXT_PUBLIC_`-Prefix versehen
- Nur in Server Components, Server Actions oder API-Routes nutzen

### Parameterisierte Abfragen

Alle Datenbankzugriffe laufen über den Supabase-JavaScript-Client, der Parameterisierung automatisch übernimmt. Niemals SQL-Strings durch String-Konkatenation mit User-Input aufbauen.

## Input-Validierung

### Zod für API-Grenzen

Alle Benutzereingaben an API-Routes und Server Actions mit Zod-Schemas validieren:

```typescript
import { z } from 'zod';

const createOrderSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().min(1).max(100),
});

// In der Server Action
const result = createOrderSchema.safeParse(formData);
if (!result.success) {
  return { error: result.error.flatten() };
}
```text
- Client-seitige Validierung gibt schnelles Feedback
- Server-seitige Validierung ist Pflicht (Client-Validierung kann umgangen werden)

## Umgebungsvariablen

| Regel | Begründung |
| --- | --- |
| Keine Secrets in Code oder Git | `.env.local` ist in `.gitignore` |
| `NEXT_PUBLIC_`-Prefix nur für öffentliche Werte | Alles mit diesem Prefix ist im Browser sichtbar |
| Service Role Key niemals mit `NEXT_PUBLIC_` | Würde in den Browser-Bundle gelangen |
| CORS korrekt für die eigene Domain konfigurieren | Verhindert unerwünschte Cross-Origin-Requests |

## Auth & Session

- Auth-Tokens in **httpOnly-Cookies** speichern — niemals in `localStorage`
- `@supabase/ssr` übernimmt das Cookie-Management korrekt
- Session auf Server-Seite immer verifizieren, nicht nur im Client

## TypeScript als Sicherheitsnetz

Strict Mode verhindert eine ganze Klasse von Bugs zur Laufzeit:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```text
- `any` vermeiden — erzwingt explizite Typen
- `unknown` statt `any` bei unbekannten Werten — Typ muss vor Nutzung eingeschränkt werden
- Generierte Supabase-Typen nutzen — keine falsch getippten Spaltennamen

## Sicherheits-Checkliste vor dem Produktions-Deploy

- [ ] RLS auf **allen** Supabase-Tabellen aktiviert
- [ ] Für jede Tabelle existieren passende RLS-Policies
- [ ] Zod-Validierung an allen API-Eingangspunkten
- [ ] `SUPABASE_SERVICE_ROLE_KEY` kein `NEXT_PUBLIC_`-Prefix
- [ ] Kein Secret in Git-History (`.env.local` in `.gitignore` geprüft)
- [ ] Auth-Tokens in httpOnly-Cookies
- [ ] CORS korrekt konfiguriert
- [ ] Keine unbeschränkten Datenbankabfragen (immer `WHERE`- oder `LIMIT`-Klauseln)

## Code-Qualität

### ESLint

ESLint läuft automatisch in der CI-Pipeline. Vor jedem Push lokal ausführen:

```bash
npm run lint
```text
Die ESLint-Konfiguration (`eslint.config.mjs`) basiert auf `eslint-config-next` und deckt Next.js-spezifische Regeln ab.

### TypeScript

TypeScript-Typprüfung vor jedem Push:

```bash
npm run typecheck
```text
Typfehler blockieren den CI-Build. Lokal reproduzieren mit:

```bash
npx tsc --noEmit
```text
### Code-Review (Vier-Augen-Prinzip)

Jeder Code-Merge auf `main` muss über einen Pull Request erfolgen. Direkte Pushes auf `main` sind nicht erlaubt. Vor dem PR-Erstellen den `@reviewer`-Copilot-Agent nutzen (Details in Kapitel 13).

### Performance-Grundregeln

**Datenbankabfragen:**

- Nur benötigte Spalten selektieren — kein `select('*')` in Produktionscode
- Indizes für Spalten in `WHERE`, `ORDER BY` und `JOIN` anlegen
- Paginierung verwenden — niemals unbegrenzte Listen laden
- Datenbank-Views für häufig genutzte komplexe Abfragen

**Next.js:**

- `next/image` für alle Bilder (automatische Optimierung, Lazy Loading)
- `next/font` für Schriften (kein FOUT/CLS)
- Schwere Komponenten mit `dynamic()` lazy-loaden
- `Suspense`-Grenzen für Streaming nutzen
- Nach jedem Build: `next build`-Output auf große Chunks prüfen

## Abhängigkeits-Sicherheit

```bash
# Veraltete Pakete prüfen
npm outdated

# Sicherheitslücken prüfen
npm audit

# Sicherheitslücken automatisch beheben (minor/patch)
npm audit fix
```text
Bei Major-Updates: manuell testen, da Breaking Changes möglich.
