# Chapter 6 – Vercel Deployment

## Overview

All WAMOCON TypeScript apps are deployed via **Vercel**. WAMOCON uses the **Vercel Hobby Plan**. Deployment is fully automated via the GitHub Actions workflow from the [`template_repo`](https://github.com/Wamocon/template_repo).

**Landing pages** are preferably published via **GitHub Pages** (Vercel is optional).

## Deployment Types

| Trigger | Deployment Type | Result |
| --- | --- | --- |
| Push to `dev` branch | **Preview** | Unique preview URL per branch |
| Merge / push to `main` | **Production** | Live under the configured domain |

## Central CI/CD Workflow

From the [`Wamocon/github_workflow`](https://github.com/Wamocon/github_workflow) repository:

```
Push to dev
  └─→ pr-autofix.yml   → Commit lint fixes automatically
  └─→ pr-checks.yml    → Validate TypeScript + ESLint
  └─→ deploy-preview.yml → Deploy Vercel preview

Merge to main
  └─→ deploy-production.yml → Vercel production deploy
```

## Required Secrets & Variables

### GitHub Organisation Level (already configured, nothing to do)

| Secret | Description |
| --- | --- |
| `VERCEL_TOKEN` | Vercel API token of the organisation |
| `VERCEL_ORG_ID` | Vercel organisation ID |

### GitHub Repository Level (once per app)

| Secret | Description | Source |
| --- | --- | --- |
| `VERCEL_PROJECT_ID` | Vercel project ID of the app | Vercel → Project Settings → General → Project ID |

## Initial Setup (once per app)

Since Vercel has no direct read access to internal GitHub repos, the following one-time workaround is needed:

### Step by Step

1. **Make repo temporarily public**
   - `Repository → Settings → General → Change visibility → Public`

2. **Import Vercel project**
   - [vercel.com](https://vercel.com) → **Add New Project** → **Import** → select repo
   - Framework is automatically detected (Next.js)
   - Perform first deployment

3. **Copy Vercel Project ID**
   - `Vercel Project → Settings → General → Project ID`

4. **Create GitHub Secret**
   - `Repository → Settings → Secrets and variables → Actions → New repository secret`
   - Name: `VERCEL_PROJECT_ID`
   - Value: the copied project ID

5. **Set repo back to internal**
   - `Repository → Settings → General → Change visibility → Internal`

6. **Enter environment variables in Vercel**
   - `Vercel Project → Settings → Environment Variables`
   - Enter all variables from `.env.local` (Supabase URL, keys, etc.)

> **Important:** Without environment variables, every build will fail.

## Environment Variables in Vercel

Set the correct scope for each variable:

| Scope | Usage |
| --- | --- |
| **Production** | Live deployment (main branch) |
| **Preview** | Dev branch deployments |
| **Development** | `vercel env pull` for local development |

## Domain Management

1. Request domain at [Strato](https://www.strato.de) via email (→ **Chapter 3, Section 2**)
2. In Vercel: `Project → Settings → Domains → Add`
3. Configure DNS records at Strato:
   - **A record** for root domain (`@`)
   - **CNAME record** for subdomain (`www`)
4. SSL certificate is automatically issued by Vercel (Let's Encrypt)

## Landing Pages: GitHub Pages (preferred) vs. Vercel

Landing pages (`[app-name]_lp`) are preferably published via **GitHub Pages**:

### GitHub Pages Setup for Landing Pages

1. In the repo: `Settings → Pages → Source: Deploy from a branch`
2. Branch: `main`, directory: `/ (root)` or `/docs`
3. GitHub Pages URL: `https://wamocon.github.io/[repo-name]/`

**Advantages of GitHub Pages:**
- Free, no build step required
- Pure HTML, directly deployable
- No Vercel project needed

**Optional Vercel:** If advanced deployment features or custom domain with SSL handling via Vercel are desired.

## Hobby Plan: Limits & Particularities

| Limit | Value |
| --- | --- |
| Bandwidth per month | 100 GB |
| Serverless Functions | 100,000 invocations/month |
| Team sharing | Not possible without upgrade |
| Deploy duration | Max. 45 minutes |

When approaching limits: coordinate with the person responsible for the Vercel account.

## Troubleshooting Deployment Failures

| Problem | Solution |
| --- | --- |
| TypeScript errors in build | Run `npm run typecheck` locally |
| Lint errors in build | Run `npm run lint` locally |
| Missing environment variable | Check Vercel → Environment Variables |
| Supabase connection error | Check Supabase URL and keys in Vercel |
| Deploy not starting | Check `VERCEL_PROJECT_ID` secret and workflow reference |

## Checklist: Vercel Setup

- [ ] Repo temporarily made public for initial import
- [ ] Vercel project imported and first deployment done
- [ ] `VERCEL_PROJECT_ID` entered as GitHub repository secret
- [ ] Repo set back to internal
- [ ] All `.env.local` variables entered in Vercel Environment Variables
- [ ] Scopes (Production/Preview/Development) set for all variables
- [ ] Domain added in Vercel (after Strato request)
- [ ] DNS configured at Strato
- [ ] Automatic deploy after merge to `main` tested
