# Kapitel 03 – GitHub Pages Workflow

## Zweck

Das Entwicklerhandbuch wird als statische Seite über GitHub Pages veröffentlicht.

## Ablauf

1. Änderungen an `index.html`, `STATUS.md` oder `chapters/` werden in den Standard-Branch gemergt.
2. Der Workflow `.github/workflows/pages.yml` wird ausgelöst.
3. Das Repository wird als GitHub-Pages-Artefakt hochgeladen.
4. GitHub deployt die Seite nach Pages.

## Betriebsnotiz

Die Seite enthält statische Inhalte. Deshalb müssen neue Statusstände per Commit oder manueller Nachfrage im Chat aktualisiert werden.
