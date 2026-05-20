# Chapter 4 – Jira & Task Management

## Usage: When Is Jira Mandatory?

| Project Type | Jira Usage |
| --- | --- |
| **Wave app development** (small, fast apps in the wave rhythm) | **Optional** – recommended but not mandatory |
| **Large projects** (not in wave rhythm, longer duration) | **Mandatory** |

For wave apps, task management can also be handled via GitHub Issues or directly through Copilot plans.

## Jira Ticket Creation

Automated ticket creation via [`wamocon_Jira_Ticket_Creation`](https://github.com/Wamocon/wamocon_Jira_Ticket_Creation) (Python).

### Ticket Types (optional, recommended standard)

| Type | Usage |
| --- | --- |
| **Story** | New feature described from the user's perspective |
| **Task** | Technical task without direct user benefit |
| **Bug** | Incorrect behaviour in an existing feature |
| **Sub-Task** | Subtask of a Story or Task |

Ticket types are a recommended standard. Project-specific deviations are possible.

## Status Workflow

```
Backlog → To Do → In Progress → In Review → Done
```

| Status | Meaning |
| --- | --- |
| **Backlog** | Idea/requirement, not yet prioritised |
| **To Do** | Prioritised, waiting for processing |
| **In Progress** | Developer is actively working on it |
| **In Review** | PR is open, code review running |
| **Done** | PR merged, feature is live |

## Jira GitHub Integration

By linking GitHub and Jira, Jira tickets are automatically updated as soon as a branch or pull request is created.

### Branch Name and Ticket Number

To activate automatic linking, the Jira ticket number must be included in the branch name:

```
feature/WMC-123-login-page
fix/WMC-456-calculation-fix
```

### Jira Automation: Automatic Status Transitions

| Action in GitHub | Ticket Status in Jira |
| --- | --- |
| Branch with ticket number created | **In Progress** |
| Pull Request opened | **In Review** |
| Pull Request merged | **Done** |

Status transitions are configured via Jira Automation and run automatically without manual intervention.

## Standard Process Flow

Binding template for all development projects:

**[wamocon.github.io/standard_prozessablauf/](https://wamocon.github.io/standard_prozessablauf/)**

Repo: [`Wamocon/standard_prozessablauf`](https://github.com/Wamocon/standard_prozessablauf)
