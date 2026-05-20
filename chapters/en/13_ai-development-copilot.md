# Chapter 8 – AI Development & Copilot Workflows

## Overview

All WAMOCON projects are optimised for AI-assisted development with **GitHub Copilot**.
Each app repository contains preconfigured agents, instructions, and global Copilot rules.

## Copilot Configuration Structure

```
.github/
├── copilot-instructions.md        # Global rules (for every Copilot interaction)
├── instructions/
│   ├── nextjs.instructions.md     # Next.js 16 App Router rules
│   ├── tailwind.instructions.md   # Tailwind CSS v4 rules
│   ├── typescript.instructions.md # TypeScript Strict Mode rules
│   └── supabase.instructions.md   # Supabase client, RLS, migrations
└── agents/
    ├── planner.agent.md           # @planner – planning without code
    ├── developer.agent.md         # @developer – implementation with verification
    └── reviewer.agent.md          # @reviewer – code review before PR
```

## The Three Copilot Agents

### `@planner` – Technical Planning

**When to use:**
- Before starting a new feature
- When requirements are unclear
- Before refactoring or migration tasks

**What it does:**
- Explore the codebase and gather context
- Identify affected files and modules
- Create a numbered implementation plan
- **Writes no code**

**Example:**

```
@planner Analyse what is needed for an authentication page with Supabase.
Create a numbered implementation plan.
```

---

### `@developer` – Structured Implementation

**When to use:**
- After planning with `@planner`
- To implement features, pages, API routes
- For database changes and migrations

**Four-phase process:**

1. **Preparation** – Read plan, understand codebase
2. **Implementation** – Step by step, fix errors immediately
3. **Verification (required)** – `typecheck` → `lint` → `build` → test locally
4. **Documentation** – Update handbook if needed

**Example:**

```
@developer Implement this plan: [paste plan from @planner]
```

---

### `@reviewer` – Code Review Before PR

**When to use:**
- Before creating a PR
- After an implementation for quality assurance
- For security and performance analysis

**What it does:**
- Structured checklist (code quality, Next.js 16, Supabase security, styling)
- Run all checks (`typecheck`, `lint`, `build`)
- Review report with status (✅ / ⚠️ / ❌)

**Example:**

```
@reviewer Review the changes in src/app/dashboard/ before the PR.
```

---

## Recommended Workflow

```
@planner  →  @developer  →  @reviewer  →  Create PR
```

1. `@planner`: Have the task analysed and an implementation plan created
2. `@developer`: Hand over the plan and have it implemented
3. `@reviewer`: Have the code checked, read the review report
4. Create PR (only when @reviewer reports no critical issues)

## Instructions – File-Specific Rules

Instructions are automatically loaded when Copilot works on files matching the `applyTo` glob pattern:

| File | Applies to | Content |
| --- | --- | --- |
| `nextjs.instructions.md` | `**/*.tsx, **/*.ts` | Next.js 16 App Router patterns, async APIs, Server/Client Components |
| `tailwind.instructions.md` | `**/*.tsx, **/*.css` | Tailwind CSS v4 utility-first, responsive design |
| `typescript.instructions.md` | `**/*.ts, **/*.tsx` | Strict mode, naming conventions, type safety |
| `supabase.instructions.md` | `**/supabase/**, **/*supabase*` | Client setup, RLS, migrations, schema |

### Creating a Custom Instruction

```markdown
---
applyTo: "**/*.tsx"
---
# Your project-specific rules here
```

## Supabase MCP – Database Context for Copilot

The **Supabase MCP (Model Context Protocol) Server** gives Copilot access to the real database schema. This enables Copilot to generate accurate code instead of guessing table structures.

### VS Code Setup (Workspace Level)

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref",
        "your-project-ref"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "your-access-token"
      }
    }
  }
}
```

### VS Code Setup (User Level, applies to all repos)

Enter in VS Code User Settings (`settings.json`) under `"mcp"`, structure as above.

### Generate Access Token

1. [supabase.com/dashboard/account/tokens](https://supabase.com/dashboard/account/tokens)
2. **Generate new token** → give a name (e.g. "MCP - Local Dev")
3. Copy token (shown only once)

### Testing the MCP Connection

In the Copilot chat:

```
Use MCP for database <project-ref>. List all schemas and tables.
```

MCP enables the following capabilities in Copilot:

| Capability | Example prompt |
| --- | --- |
| List tables | "What tables exist in the test schema?" |
| Describe table | "Show me the columns of the orders table" |
| Generate SQL | "Write a query for all open orders with user info" |
| Scaffold Server Action | "Create a Server Action that loads the user profile by ID" |
| Generate RLS policy | "Create an RLS policy so users only see their own data" |

### MCP Security Rules

- Always use `--read-only` (unless write access is explicitly needed)
- Never commit token, store in user-level settings or environment variables
- Use `test` schema for AI-assisted development, not `prod`
- Review all generated SQL statements before execution
- Rotate tokens regularly

## Copilot Instructions at User Level

Every developer can define personal Copilot instructions that apply to all repos:

**Windows path:**
```
C:\Users\<user>\AppData\Roaming\Code\User\prompts\my-default.instructions.md
```

**Example content:**

```markdown
---
description: "Applies to all repos"
---
- Always follow TypeScript strict mode
- For database tasks use MCP with the correct project-ref
- Prefer minimal, safe changes
- Comment assumptions
```

## Troubleshooting Copilot Issues

| Problem | Solution |
| --- | --- |
| Agent ignores instructions | Check `applyTo` glob pattern, make it broader if needed (`**/*.ts` instead of `src/**/*.ts`) |
| MCP not connecting | Check access token and project-ref in settings |
| Agent writes incorrect code | Provide more context, reference the requirements document or specific files |
| Vercel build fails after implementation | Run `@reviewer` before creating PR |
