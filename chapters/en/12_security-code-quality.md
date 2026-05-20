# Chapter 7 – Security & Code Quality

## Principles

Security is not added retrospectively, but built in from the start. Every new app must meet the following minimum standards before going to production.

## Supabase Security

### Row Level Security (RLS) – Required

RLS must be enabled for **every table**. Without RLS, every authenticated user has unrestricted access.

```sql
-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their own data
CREATE POLICY "Read own data"
  ON public.profiles FOR SELECT
  USING (auth.uid() = user_id);
```

### Service Role Key

- **Never** use `SUPABASE_SERVICE_ROLE_KEY` in browser code
- Never give it the `NEXT_PUBLIC_` prefix
- Only use in Server Components, Server Actions, or API routes

### Parameterised Queries

All database accesses run through the Supabase JavaScript client, which handles parameterisation automatically. Never build SQL strings by concatenating user input.

## Input Validation

### Zod for API Boundaries

Validate all user inputs at API routes and Server Actions with Zod schemas:

```typescript
import { z } from 'zod';

const createOrderSchema = z.object({
  productId: z.string().uuid(),
  quantity: z.number().int().min(1).max(100),
});

// In the Server Action
const result = createOrderSchema.safeParse(formData);
if (!result.success) {
  return { error: result.error.flatten() };
}
```

- Client-side validation provides quick feedback
- Server-side validation is mandatory (client validation can be bypassed)

## Environment Variables

| Rule | Reason |
| --- | --- |
| No secrets in code or Git | `.env.local` is in `.gitignore` |
| `NEXT_PUBLIC_` prefix only for public values | Everything with this prefix is visible in the browser |
| Service role key never with `NEXT_PUBLIC_` | Would end up in the browser bundle |
| Configure CORS correctly for own domain | Prevents unwanted cross-origin requests |

## Auth & Session

- Store auth tokens in **httpOnly cookies**, never in `localStorage`
- `@supabase/ssr` handles cookie management correctly
- Always verify session on the server side, not just in the client

## TypeScript as a Safety Net

Strict Mode prevents a whole class of runtime bugs:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

- Avoiding `any` enforces explicit types
- `unknown` instead of `any` for unknown values; type must be narrowed before use
- Use generated Supabase types, no incorrectly typed column names

## Security Checklist Before Production Deploy

- [ ] RLS enabled on **all** Supabase tables
- [ ] Appropriate RLS policies exist for each table
- [ ] Zod validation at all API entry points
- [ ] `SUPABASE_SERVICE_ROLE_KEY` has no `NEXT_PUBLIC_` prefix
- [ ] No secrets in Git history (`.env.local` checked in `.gitignore`)
- [ ] Auth tokens in httpOnly cookies
- [ ] CORS correctly configured
- [ ] No unbounded database queries (always use `WHERE` or `LIMIT` clauses)

## Code Quality

### ESLint

ESLint runs automatically in the CI pipeline. Run locally before every push:

```bash
npm run lint
```

The ESLint configuration (`eslint.config.mjs`) is based on `eslint-config-next` and covers Next.js-specific rules.

### TypeScript

TypeScript type check before every push:

```bash
npm run typecheck
```

Type errors block the CI build. Reproduce locally with:

```bash
npx tsc --noEmit
```

### Code Review (Four-Eyes Principle)

Every code merge to `main` must go through a pull request. Direct pushes to `main` are not allowed. Use the `@reviewer` Copilot agent before creating the PR (details in Chapter 8).

### Performance Guidelines

**Database queries:**

- Select only the required columns, no `select('*')` in production code
- Create indexes for columns in `WHERE`, `ORDER BY`, and `JOIN`
- Use pagination, never load unbounded lists
- Use database views for frequently used complex queries

**Next.js:**

- `next/image` for all images (automatic optimisation, lazy loading)
- `next/font` for fonts (no FOUT/CLS)
- Lazy-load heavy components with `dynamic()`
- Use `Suspense` boundaries for streaming
- After every build: check `next build` output for large chunks

## Dependency Security

```bash
# Check outdated packages
npm outdated

# Check security vulnerabilities
npm audit

# Automatically fix vulnerabilities (minor/patch)
npm audit fix
```

For major updates: test manually, as breaking changes are possible.
