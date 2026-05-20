# Chapter 5 – Supabase Cloud Project

## What is Supabase?

WAMOCON uses **Supabase Pro** as the primary Backend-as-a-Service for all apps. It provides:

- **PostgreSQL database** with full SQL access
- **Auth**, user authentication (email, OAuth, magic links)
- **Row Level Security (RLS)**, fine-grained access control at the database level
- **Storage**, file storage (images, documents)
- **Edge Functions**, serverless functions (when needed)
- **REST & Realtime API**, automatically generated from the database schema

## 1. Request (Required Before Development Start)

The Supabase Cloud project is **requested via email**, no self-service.

**Timing:** Directly after approval of the requirements document (→ **Chapter 3, Section 2**)

**Information in the email:**

- App name (identical to the GitHub repo name)

> By requesting early, there is no waiting time just before go-live.

## 2. Setup (env.local)

After project creation in the Supabase Dashboard, retrieve the following credentials under **Project Settings → API** and enter them in `.env.local`:

```env
# Supabase Cloud
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxxx
SUPABASE_SERVICE_ROLE_KEY=xxxx
DATABASE_URL=postgresql://postgres:xxxx@db.xxxx.supabase.co:5432/postgres

# Schema (default: public)
SUPABASE_DB_SCHEMA=public
```

| Variable | Source in Supabase | Usage |
| --- | --- | --- |
| `NEXT_PUBLIC_SUPABASE_URL` | Project Settings → API → Project URL | Connection endpoint |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Project Settings → API → anon public | Client-side access (restricted) |
| `SUPABASE_SERVICE_ROLE_KEY` | Project Settings → API → service_role | Server-side full access |
| `DATABASE_URL` | Project Settings → Database → Connection string | Direct database connection (CLI, MCP) |

> **Security:** Never commit `.env.local` to the repository (check `.gitignore`).
> **Never** give `SUPABASE_SERVICE_ROLE_KEY` the `NEXT_PUBLIC_` prefix.

## 3. Schemas

### Recommended Schema Structure

| Schema | Purpose |
| --- | --- |
| `[appname]_dev` | Development and test data (replaces `public`) |
| `[appname]_test` | Separate test schema |
| `[appname]_prod` | Production data (separated from test data) |

The schema structure is recommended and can be adjusted on a project-specific basis.

### Create Schema and Set Permissions

```sql
-- Example for app "carman"
CREATE SCHEMA IF NOT EXISTS carman_dev;
CREATE SCHEMA IF NOT EXISTS carman_test;
CREATE SCHEMA IF NOT EXISTS carman_prod;

GRANT USAGE ON SCHEMA carman_dev TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA carman_test TO anon, authenticated, service_role;
GRANT USAGE ON SCHEMA carman_prod TO anon, authenticated, service_role;

GRANT ALL ON ALL TABLES IN SCHEMA carman_dev TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA carman_test TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA carman_prod TO anon, authenticated, service_role;
```

Make schemas accessible via the API: **Project Settings → API → Exposed schemas** → add schema names.

## 4. Database Migrations

Schema changes can be made in two ways.

**Option 1: Migration Files** (recommended, versionable)

**GitHub Copilot handles the creation and execution of migrations** based on the requirements document.

```bash
# Create migration (Copilot generates the SQL content)
npx supabase migration new <migration-name>
# Creates: supabase/migrations/<timestamp>_<name>.sql

# Apply migrations locally
npx supabase db reset

# Apply migrations to Supabase Cloud
npx supabase db push

# Check migration status
npx supabase migration list
```

**Option 2: SQL Editor** (for quick adjustments)

Schema changes can also be made directly in the SQL Editor of the Supabase Dashboard. In this case, the change should subsequently be documented as a migration file.

**Important:** Always commit migration files in `supabase/migrations/` to Git. Never modify existing migration files retroactively.

## 5. Row Level Security (RLS)

RLS must be enabled for **every table**. Copilot is instructed to always enable RLS and never leave it disabled.

```sql
-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users see only their own data
CREATE POLICY "Read own data"
  ON public.profiles FOR SELECT
  USING (auth.uid() = user_id);
```

RLS policies are versioned as part of migrations.

## 6. Supabase Auth

Auth configuration via the Supabase Dashboard:
- Enable/disable email / password
- Configure OAuth providers (Google, GitHub, etc.)
- Customise email templates

In the app, `@supabase/ssr` is used for server-side auth integration (details → **Chapter 2, Tech Stack**).

## 7. Local Supabase Instance (Fallback & Development Phase)

### When to Use?

- Supabase Cloud project still being requested (→ Chapter 3, Section 1)
- Offline development and rapid prototyping without cloud connection

### Local Instances via localSupabaseDB

The repo [`Wamocon/localSupabaseDB`](https://github.com/Wamocon/localSupabaseDB) enables running multiple local Supabase instances in parallel for different app developments:

- Each app gets its own isolated instance
- Setup as per the [README.md in the localSupabaseDB repo](https://github.com/Wamocon/localSupabaseDB/blob/main/README.md)
- Point `.env.local` to the local instance URL instead of Supabase Cloud

```bash
# Start local instance
npx supabase start

# Show status and local credentials
npx supabase status
```

Enter local credentials in `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=<from npx supabase status>
SUPABASE_SERVICE_ROLE_KEY=<from npx supabase status>
```

### Hardware Limit: Huawei Laptop RAM

With more than **2 parallel local Supabase instances** and **2 simultaneously running apps**, the Huawei laptop reaches its RAM limits.

Symptoms: Slow response times, app freezes, instance crashes.

**Recommendation:** Run a maximum of 2 local Supabase instances + 2 active apps simultaneously. Actively stop instances that are not needed.

### Switching from Local to Supabase Cloud

Once the Supabase Cloud project is approved:

1. Update `.env.local` variables to the cloud values
2. Apply locally developed migrations to Supabase Cloud: `npx supabase db push`
3. Stop local instance: `npx supabase stop`
4. Free up resources

## 8. Supabase MCP for GitHub Copilot

The Supabase MCP (Model Context Protocol) server gives Copilot access to the real database schema.

Configuration details → **Chapter 8, AI Development & Copilot Workflows**

## 9. Checklist: Supabase Setup

- [ ] Supabase Cloud project requested via email (directly after requirements approval)
- [ ] Project created and status "Healthy"
- [ ] `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL` entered in `.env.local`
- [ ] All variables stored as Vercel Environment Variables (→ Chapter 6)
- [ ] `SUPABASE_SERVICE_ROLE_KEY` has **no** `NEXT_PUBLIC_` prefix
- [ ] `.env.local` present in `.gitignore`
- [ ] RLS enabled for all tables
- [ ] First migration created and committed in `supabase/migrations/`
- [ ] MCP configured for local Copilot tools (→ Chapter 8)
