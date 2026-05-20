# Chapter 10 – Glossary & References

## WAMOCON-Specific Terms

| Term | Meaning |
| --- | --- |
| **Wave** | Time-bundled release cycle in which several apps are developed and published in parallel |
| **Requirements Document** | Structured document describing a new app (purpose, functions, database schema), basis for Copilot-assisted development |
| **LP** | Landing Page – static HTML page presenting an app |
| **EHB** | Developer Handbook (this document) |
| **WMC Standard** | Internal WAMOCON conventions for naming, processes, and quality |
| **Huawei Laptop** | The local development laptop that reaches RAM limits with more than 2 parallel Supabase instances |
| **template_repo** | Base repository for all new WAMOCON apps, contains complete configuration |

## Technical Glossary

| Term | Meaning |
| --- | --- |
| **App Router** | Next.js routing system based on the `src/app/` directory (from Next.js 13) |
| **CI/CD** | Continuous Integration / Continuous Deployment – automated build, test, and deploy pipeline |
| **CNAME** | DNS record (Canonical Name) for subdomain forwarding |
| **Edge Function** | Serverless function executed at network edges (near the user) |
| **ESLint** | JavaScript/TypeScript linting tool for code quality assurance |
| **GitHub Pages** | Free hosting for static sites directly from a GitHub repository |
| **MCP** | Model Context Protocol – standard for connecting AI tools to external data sources |
| **Migration** | Versioned SQL file describing database schema changes |
| **npm** | Node Package Manager – package manager for Node.js/JavaScript |
| **PostgREST** | Automatically generated REST API based on PostgreSQL schemas (part of Supabase) |
| **PR** | Pull Request – request to merge branches |
| **RLS** | Row Level Security – fine-grained access control in PostgreSQL at row level |
| **SSR** | Server-Side Rendering – HTML is generated on the server |
| **Tailwind CSS** | Utility-First CSS framework |
| **Turbopack** | Fast JavaScript bundler (Next.js dev server) |
| **TypeScript** | Typed JavaScript – prevents runtime errors through static type checking |
| **Zod** | TypeScript schema validation library for runtime validation |

## Tool Reference

| Tool | Purpose | Link |
| --- | --- | --- |
| **GitHub** | Repository hosting, CI/CD, issues | [github.com/Wamocon](https://github.com/Wamocon) |
| **GitHub Copilot** | Primary development tool (AI code assistant) | [github.com/features/copilot](https://github.com/features/copilot) |
| **Vercel** | App deployment and hosting | [vercel.com](https://vercel.com) |
| **Supabase** | Backend-as-a-Service (PostgreSQL, Auth, Storage), Pro version | [supabase.com](https://supabase.com) |
| **Strato** | Domain registrar for WAMOCON domains | [strato.de](https://www.strato.de) |
| **Jira** | Project management and task tracking (optional for waves) | internal |
| **OneDrive** | Storage for requirements documents | internal |
| **n8n** | Workflow automation (landing page generation, marketing) | internal |

## External Documentation

| Technology | Link |
| --- | --- |
| Next.js Docs | [nextjs.org/docs](https://nextjs.org/docs) |
| Supabase Docs | [supabase.com/docs](https://supabase.com/docs) |
| Vercel Docs | [vercel.com/docs](https://vercel.com/docs) |
| Tailwind CSS v4 Docs | [tailwindcss.com/docs](https://tailwindcss.com/docs) |
| TypeScript Docs | [typescriptlang.org/docs](https://www.typescriptlang.org/docs/) |
| Supabase MCP | [github.com/supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) |
| GitHub Copilot Customization | [docs.github.com/en/copilot/customizing-copilot](https://docs.github.com/en/copilot/customizing-copilot) |
| awesome-copilot | [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot) |

## Internal References

| Resource | Link |
| --- | --- |
| Standard Process Flow | [wamocon.github.io/standard_prozessablauf/](https://wamocon.github.io/standard_prozessablauf/) |
| template_repo (base for all new apps) | [github.com/Wamocon/template_repo](https://github.com/Wamocon/template_repo) |
| github_workflow (CI/CD standards) | [github.com/Wamocon/github_workflow](https://github.com/Wamocon/github_workflow) |
| localSupabaseDB (local database instances) | [github.com/Wamocon/localSupabaseDB](https://github.com/Wamocon/localSupabaseDB) |
| WMC Requirements Portal | [github.com/Wamocon/WMC-Anforderungsportal](https://github.com/Wamocon/WMC-Anforderungsportal) |
| wamohub (app template & hub) | [github.com/Wamocon/wamohub](https://github.com/Wamocon/wamohub) |
| github_workflow → Workflow Guide | [github.com/Wamocon/github_workflow/blob/main/docs/workflow-guide.md](https://github.com/Wamocon/github_workflow/blob/main/docs/workflow-guide.md) |
| github_workflow → Supabase & Vercel Linking | [github.com/Wamocon/github_workflow/blob/main/docs/supabase-vercel-linking.md](https://github.com/Wamocon/github_workflow/blob/main/docs/supabase-vercel-linking.md) |
| github_workflow → MCP Setup | [github.com/Wamocon/github_workflow/blob/main/docs/mcp-setup.md](https://github.com/Wamocon/github_workflow/blob/main/docs/mcp-setup.md) |
| github_workflow → Tips & Best Practices | [github.com/Wamocon/github_workflow/blob/main/docs/tips-and-best-practices.md](https://github.com/Wamocon/github_workflow/blob/main/docs/tips-and-best-practices.md) |
| Developer Handbook GitHub Pages | [wamocon.github.io/wamocon_entwicklerhandbuch/](https://wamocon.github.io/wamocon_entwicklerhandbuch/) |
