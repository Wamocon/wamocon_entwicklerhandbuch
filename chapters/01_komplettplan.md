# Kapitel 01 – Kompletter Plan für das WAMOCON Entwicklerhandbuch

## Ziel

Das Entwicklerhandbuch soll GitHub-Struktur, Tech-Stack, Entwicklungsprozess, Jira, Supabase, Vercel, Sicherheit, KI-Workflows, App-Katalog und Referenzen dokumentieren.

## Kapitelübersicht

1. GitHub & Repository-Struktur
2. Tech Stack & Standards
3. Entwicklungsprozess
4. Jira & Aufgabenmanagement
5. Supabase Cloud Projekt
6. Vercel Deployment
7. Sicherheit & Code-Qualität
8. KI-Entwicklung & Copilot-Workflows
9. Produkt-Ökosystem
10. Glossar & Referenzen

## Ergänzung für Kapitel 5

### 5.5 Lokale Supabase Instanz (Fallback & Entwicklungsphase)

- Nutzen, wenn noch kein Supabase-Cloud-Projekt existiert oder die Beantragung läuft
- Mehrere lokale Instanzen können über `localSupabaseDB` parallel betrieben werden
- Jede App erhält eine isolierte lokale Instanz mit eigener Konfiguration
- Bei mehr als zwei parallelen Supabase-Instanzen und zwei laufenden Apps stößt die Huawei-Hardware an RAM-Grenzen
- Empfehlung: maximal zwei lokale Instanzen plus zwei aktive Apps gleichzeitig betreiben
- Sobald das Cloud-Projekt verfügbar ist, auf Supabase Cloud umstellen und lokale Ressourcen freigeben

## Pflegehinweis

Der komplette fachliche Ausbau der Kapitel erfolgt in den einzelnen Markdown-Dateien. Diese Datei dient als kompakter Gesamtplan und Einstieg.
