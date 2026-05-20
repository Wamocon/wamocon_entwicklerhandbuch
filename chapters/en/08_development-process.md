# Chapter 3 – Development Process

> **Important:** All app development at WAMOCON is carried out entirely with **GitHub Copilot**. Copilot is not just an aid, but the primary development tool, from planning through implementation to migrations and deployment configurations.

## Overview: From Idea to Production

```
Product idea & requirements creation (manual)
       │
       ▼
Store requirements document in OneDrive & submit for approval
       │
       ▼
Wait for approval
       │
       ├─→ Request Supabase Cloud project via email (→ Chapter 5)
       └─→ Request Strato domain via email (→ Chapter 6)
                │
                ▼
Create new GitHub repository from template_repo, create dev branch, load requirements into Copilot
       │
       ▼
Copilot creates development plan → iterative implementation
       │
       ▼
Local tests → PR dev → main → Vercel production
       │
       ▼
Generate landing page (prefer GitHub Pages, Vercel optional)
```

---

## 1. Product Idea & Requirements Creation

The ideation and initial requirements definition are done **manually by the developer**.

### Creating the Requirements Document

**Preferred way:** Use the **[WMC Requirements Portal](https://github.com/Wamocon/WMC-Anforderungsportal)**.

**Alternative way:** Create requirements document manually and submit via email.

The requirements document contains:
- App name and brief description
- Target audience and main benefit
- Core functions and requirements
- Desired database schema (rough)
- Technical framework conditions

### Storage in OneDrive

The completed requirements document is stored in **OneDrive**:

```
OneDrive / Wave [Number] / [App-Name] / Requirements_[App-Name].docx
```

**Important:** Development begins **only after approval** of the requirements document.

---

## 2. After Approval: Request Infrastructure

Directly after the requirements document is approved, to avoid waiting time before go-live:

### Request Supabase Cloud Project

The Supabase Cloud project is **requested via email** (no self-service).

Information in the email:
- App name (identical to the planned repo name)

Details on setup after approval → **Chapter 5, Supabase Cloud Project**

### Request Strato Domain

The domain for the app is **requested via email at Strato**.

- Specify domain name (e.g. `app-name.de` or `app-name.wamocon.de`)
- After allocation, the domain is configured in Vercel → **Chapter 6, Vercel Deployment**

---

## 3. Development Start: Template Repo & GitHub Copilot

### Create Repository

1. On GitHub: [`Wamocon/template_repo`](https://github.com/Wamocon/template_repo) → **"Use this template"** → **"Create a new repository"**
2. Create repository in the `Wamocon` organisation
3. Set name according to naming convention (→ **Chapter 1**)
4. Visibility: **Internal**
5. Create `dev` branch, `main` remains protected

### Load Requirements Document into GitHub Copilot

Load the approved requirements document as context into GitHub Copilot and instruct Copilot to create a comprehensive development plan:

```
Load the requirements document from OneDrive and create a complete
development plan for the app [App-Name] based on this document:

- Database schema & migrations (tables, columns, RLS policies)
- Component structure (pages, UI components, layouts)
- API endpoints and Server Actions
- Milestones & task packages in logical order
```

### Develop with Copilot

Copilot takes over:
- Creating and executing database migrations
- Implementing components and pages
- Writing API routes and Server Actions
- Adjusting configuration files
- Configuring deployment workflows

**Developer role:** Define requirements, steer Copilot, review and approve output.

Development runs **iteratively along the Copilot plan**:
1. Read plan step
2. Instruct Copilot to implement this step
3. Test output locally
4. If issues: correct Copilot
5. Move to next step

---

## 4. Local Development & Database Migrations

### Setting Up the Environment

```bash
# Clone repository
git clone https://github.com/Wamocon/<repo-name>.git
cd <repo-name>

# Switch to dev branch
git checkout dev

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Enter Supabase credentials in .env.local (→ Chapter 5)

# Start development server
npm run dev
```

### Supabase Fallback: Local Instance

While the Supabase Cloud project is still **being requested**, use the local instance:
→ **Chapter 5.7, Local Supabase Instance**

### Database Migrations

GitHub Copilot creates and executes migrations directly from within the app to Supabase Cloud:

```bash
# Create migration (Copilot generates the SQL content)
npx supabase migration new <migration-name>

# Apply migration locally (fallback on local instance)
npx supabase db reset

# Apply migration to Supabase Cloud
npx supabase db push
```

Migration history is versioned in the repo under `/supabase/migrations/`.

### Local Quality Check Before Commit

```bash
npm run typecheck   # TypeScript errors
npm run lint        # Lint issues
npm run dev         # Manual testing
```

---

## 5. CI/CD Pipeline (automatic)

### On Push to `dev`: Preview Deployment

```
Push to dev
  └─→ pr-autofix: ESLint --fix (commits back)
  └─→ pr-checks: TypeScript + ESLint validate
  └─→ Vercel: Preview deployment
```

### On Merge to `main`: Production Deployment

```
PR from dev → main merged
  └─→ Vercel: Production deployment
```

Details → **Chapter 6, Vercel Deployment**

---

## 6. Generate Landing Page

Each app gets its own landing page repository (`[app-name]_lp`).

### Landing Page Generation with Copilot

```
Create a static HTML landing page for the app [App-Name] based on the
requirements document. The landing page should include:
- Hero section with app name and tagline
- Feature overview (3–5 key features)
- Screenshot or mockup area
- Call-to-action with link to the app
- Footer with imprint and privacy policy links
```

### Publish via GitHub Pages

1. Create new repo `[app-name]_lp` in the `Wamocon` organisation
2. `Settings → Pages → Source: Deploy from a branch`
3. Branch: `main`, directory: `/ (root)`
4. URL: `https://wamocon.github.io/[repo-name]/`
