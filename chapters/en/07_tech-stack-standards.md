# Chapter 2 – Tech Stack & Standards

## Overview

All WAMOCON web applications are based on a unified tech stack.
This tech stack is the standard for all new apps. Deviations are possible and can be justified on a topic-specific basis.

| Layer | Technology | Version |
| --- | --- | --- |
| Framework | Next.js (App Router) | 16.x |
| Language | TypeScript (strict mode) | 5.x |
| Styling | Tailwind CSS | v4 |
| Backend & Database | Supabase (PostgreSQL, Auth, RLS) | 2.x |
| Deployment | Vercel | – |
| Package Manager | npm | – |
| Linter | ESLint | 9.x |
| Dev Server | Next.js with Turbopack | – |
| E2E Tests | Playwright | – |

## Next.js 16, App Router

All apps use the **App Router** (`src/app/`). The Pages Router is not used.

### Key Rules

- **Server Components are the default**, only add `"use client"` when interactivity is required
- Extract Server Actions into separate files (`actions.ts` in the feature folder)
- Create `loading.tsx` and `error.tsx` for each route segment
- Validate form inputs on both client and server side
- Use `revalidatePath` / `revalidateTag` instead of manual cache-busting
- Use `next/image` for all images (automatic optimisation)
- Use `next/font` for fonts (no layout shift)

### Available npm Scripts

| Command | Description |
| --- | --- |
| `npm run dev` | Start dev server with Turbopack (hot reload) |
| `npm run build` | Create production build |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run typecheck` | Run TypeScript type check |
| `npm run db:start` | Start local Supabase instance |
| `npm run db:stop` | Stop local Supabase instance |
| `npm run db:reset` | Reset local database |
| `npm run db:status` | Check status of local Supabase |

## TypeScript

All projects use TypeScript in **Strict Mode** (`strict: true` in `tsconfig.json`).

### Conventions

- **Avoid `any`**, use `unknown` and narrow the type
- **Zod for runtime validation** at API boundaries
- **Prefer interfaces** over `type` for object shapes (better error messages)
- **Export types centrally** per feature in `types.ts`
- Use generated Supabase types:

```typescript
import { Database } from '@/types/supabase';
const supabase = createServerClient<Database>(...);
```

## Tailwind CSS v4

All apps use Tailwind CSS v4 with the PostCSS plugin (`@tailwindcss/postcss`).

### Core Rules

- Utility-first approach, no separate CSS files except for global styles
- Responsive design using Tailwind's standard breakpoints
- No magic numbers, use Tailwind scale values
- Follow the WAMOCON design system (dark blue gradient, accent colour `#1fd0b0`) from Chapter 5

## Supabase

Supabase provides PostgreSQL database, authentication, and Row Level Security.
Configuration and usage details in **Chapter 5, Supabase Cloud Project**.

### Supabase Client Rules

- Use **`createServerClient`** in Server Components and Server Actions
- Use **`createBrowserClient`** only in Client Components
- Always check errors:

```typescript
const { data, error } = await supabase.from('users').select('*');
if (error) throw error;
```

## Dependencies (Standard)

### Production Dependencies

| Package | Purpose |
| --- | --- |
| `next` | Framework |
| `react` / `react-dom` | UI library |
| `@supabase/supabase-js` | Supabase JavaScript client |
| `@supabase/ssr` | Supabase SSR helpers for Next.js |
| `lucide-react` | Icon library |

### Development Dependencies

| Package | Purpose |
| --- | --- |
| `typescript` | Language compilation |
| `eslint` | Linter |
| `eslint-config-next` | Next.js ESLint configuration |
| `tailwindcss` | CSS framework |
| `@tailwindcss/postcss` | Tailwind v4 PostCSS plugin |
| `@types/react` / `@types/node` | TypeScript types |

## Environment Variables

Every project has a `.env.example` file as a template. The actual `.env.local` is never committed to Git.

### Standard Variables

```env
# Next.js
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_SITE_NAME=<App-Name>

# Supabase (local)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<from npx supabase status>
SUPABASE_SERVICE_ROLE_KEY=<from npx supabase status>

# Supabase (Cloud)
# NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key>
# SUPABASE_SERVICE_ROLE_KEY=<service-role-key>

# Schema
SUPABASE_DB_SCHEMA=public
```

**Important:** The `NEXT_PUBLIC_` prefix means the variable is visible in the browser.
The `SUPABASE_SERVICE_ROLE_KEY` must **never** have the `NEXT_PUBLIC_` prefix.

## Global Tools (Developer Machine)

Every developer should have the following tools installed:

```bash
# Node.js via nvm (Version 20)
nvm install 20
nvm use 20

# Vercel CLI
npm install -g vercel

# Supabase CLI
npm install -g supabase
```

## VS Code Extensions (Recommended)

| Extension | Purpose |
| --- | --- |
| GitHub Copilot | AI code assistant |
| GitHub Copilot Chat | AI chat interface |
| ESLint | Linting |
| Prettier | Code formatting |
| Tailwind CSS IntelliSense | Tailwind autocomplete |
| Error Lens | Inline error display |
| GitLens | Git blame & history |
| Supabase | Supabase integration |

## VS Code Workspace Settings (Recommended)

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
```
