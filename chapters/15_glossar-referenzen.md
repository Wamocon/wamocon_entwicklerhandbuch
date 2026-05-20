# Kapitel 5, Glossar & Referenzen

## WAMOCON-spezifische Begriffe

| Begriff | Bedeutung |
| --- | --- |
| **Welle** | Zeitlich gebündelter Release-Zyklus, in dem mehrere Apps parallel entwickelt und veröffentlicht werden |
| **Anforderungsdokument** | Strukturiertes Dokument, das eine neue App beschreibt (Zweck, Funktionen, Datenbankschema), Basis für die Copilot-gestützte Entwicklung |
| **LP** | Landing Page, statische HTML-Seite zur Vorstellung einer App |
| **EHB** | Entwicklerhandbuch (dieses Dokument) |
| **WMC-Standard** | Interne WAMOCON-Konventionen für Benennung, Prozesse und Qualität |
| **Huawei-Laptop** | Der lokale Entwicklungs-Laptop, der bei mehr als 2 parallelen Supabase-Instanzen an RAM-Grenzen stößt |
| **template_repo** | Basis-Repository für alle neuen WAMOCON-Apps, enthält vollständige Konfiguration |

## Technisches Glossar

| Begriff | Bedeutung |
| --- | --- |
| **App Router** | Next.js-Routing-System basierend auf dem `src/app/`-Verzeichnis (ab Next.js 13) |
| **CI/CD** | Continuous Integration / Continuous Deployment, automatisierte Build-, Test- und Deploy-Pipeline |
| **CNAME** | DNS-Eintrag (Canonical Name) für Subdomain-Weiterleitung |
| **Edge Function** | Serverless-Funktion die an Netzwerk-Edges (nahe dem Nutzer) ausgeführt wird |
| **ESLint** | JavaScript/TypeScript Linting-Tool zur Code-Qualitätssicherung |
| **GitHub Pages** | Kostenloses Hosting für statische Seiten direkt aus einem GitHub-Repository |
| **MCP** | Model Context Protocol, Standard für die Verbindung von KI-Tools mit externen Datenquellen |
| **Migration** | Versionierte SQL-Datei, die Datenbankschema-Änderungen beschreibt |
| **npm** | Node Package Manager, Paket-Manager für Node.js/JavaScript |
| **PostgREST** | Automatisch generierte REST API auf Basis von PostgreSQL-Schemas (Teil von Supabase) |
| **PR** | Pull Request, Anfrage zum Zusammenführen von Branches |
| **RLS** | Row Level Security, feingranulare Zugriffssteuerung in PostgreSQL auf Zeilenebene |
| **SSR** | Server-Side Rendering, HTML wird auf dem Server generiert |
| **Tailwind CSS** | Utility-First CSS-Framework |
| **Turbopack** | Schneller JavaScript-Bundler (Next.js Dev-Server) |
| **TypeScript** | Typisiertes JavaScript, verhindert Laufzeitfehler durch statische Typprüfung |
| **Zod** | TypeScript-Schema-Validierungsbibliothek für Runtime-Validierung |

## Tool-Referenz

| Tool | Zweck | Link |
| --- | --- | --- |
| **GitHub** | Repository-Hosting, CI/CD, Issues | [github.com/Wamocon](https://github.com/Wamocon) |
| **GitHub Copilot** | Primäres Entwicklungswerkzeug (KI-Code-Assistent) | [github.com/features/copilot](https://github.com/features/copilot) |
| **Vercel** | App-Deployment und Hosting | [vercel.com](https://vercel.com) |
| **Supabase** | Backend-as-a-Service (PostgreSQL, Auth, Storage), Pro-Version | [supabase.com](https://supabase.com) |
| **Strato** | Domain-Registrar für WAMOCON-Domains | [strato.de](https://www.strato.de) |
| **Jira** | Projektmanagement und Aufgabenverwaltung (optional bei Wellen) | intern |
| **OneDrive** | Ablage von Anforderungsdokumenten | intern |
| **n8n** | Workflow-Automatisierung (Landing-Page-Generierung, Marketing) | intern |

## Externe Dokumentationen

| Technologie | Link |
| --- | --- |
| Next.js Docs | [nextjs.org/docs](https://nextjs.org/docs) |
| Supabase Docs | [supabase.com/docs](https://supabase.com/docs) |
| Vercel Docs | [vercel.com/docs](https://vercel.com/docs) |
| Tailwind CSS v4 Docs | [tailwindcss.com/docs](https://tailwindcss.com/docs) |
| TypeScript Docs | [typescriptlang.org/docs](https://www.typescriptlang.org/docs/) |
| Supabase MCP | [github.com/supabase-community/supabase-mcp](https://github.com/supabase-community/supabase-mcp) |
| GitHub Copilot Customization | [docs.github.com/en/copilot/customizing-copilot](https://docs.github.com/en/copilot/customizing-copilot) |
| awesome-copilot | [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot) |

## Interne Referenzen

| Ressource | Link |
| --- | --- |
| Standard-Prozessablauf | [wamocon.github.io/standard_prozessablauf/](https://wamocon.github.io/standard_prozessablauf/) |
| template_repo (Basis für alle neuen Apps) | [github.com/Wamocon/template_repo](https://github.com/Wamocon/template_repo) |
| github_workflow (CI/CD-Standards) | [github.com/Wamocon/github_workflow](https://github.com/Wamocon/github_workflow) |
| localSupabaseDB (lokale Datenbankinstanzen) | [github.com/Wamocon/localSupabaseDB](https://github.com/Wamocon/localSupabaseDB) |
| WMC-Anforderungsportal | [github.com/Wamocon/WMC-Anforderungsportal](https://github.com/Wamocon/WMC-Anforderungsportal) |
| wamohub (App-Template & Hub) | [github.com/Wamocon/wamohub](https://github.com/Wamocon/wamohub) |
| github_workflow → Workflow Guide | [github.com/Wamocon/github_workflow/blob/main/docs/workflow-guide.md](https://github.com/Wamocon/github_workflow/blob/main/docs/workflow-guide.md) |
| github_workflow → Supabase & Vercel Linking | [github.com/Wamocon/github_workflow/blob/main/docs/supabase-vercel-linking.md](https://github.com/Wamocon/github_workflow/blob/main/docs/supabase-vercel-linking.md) |
| github_workflow → MCP Setup | [github.com/Wamocon/github_workflow/blob/main/docs/mcp-setup.md](https://github.com/Wamocon/github_workflow/blob/main/docs/mcp-setup.md) |
| github_workflow → Tips & Best Practices | [github.com/Wamocon/github_workflow/blob/main/docs/tips-and-best-practices.md](https://github.com/Wamocon/github_workflow/blob/main/docs/tips-and-best-practices.md) |
| Entwicklerhandbuch GitHub Pages | [wamocon.github.io/wamocon_entwicklerhandbuch/](https://wamocon.github.io/wamocon_entwicklerhandbuch/) |
