# rivecon-GmbH/.github

Zentrale Workflows und Vorlagen für alle Repositories der rivecon GmbH (Odoo 19/20, Deployment auf Odoo.sh).
Die Logik liegt nur hier, die einzelnen Repos rufen sie auf.

> **Öffentliches Repo, bewusst:** Es enthält nur Prüf-Konfiguration, keine Geheimnisse. Es ist öffentlich,
> damit auch Repos aus dem persönlichen GitHub-Account (noch nicht umgezogene Kundenrepos) die Workflows
> aufrufen können. **Sobald alle Repos in der Organisation liegen, kann dieses Repo auf privat gestellt
> werden** (dann unter *Settings → Actions → General → Access* den Zugriff für Repos der Organisation erlauben).

## Code-Scan (`odoo-code-scan.yml`)

Rein **informativ**: jeder Prüfschritt läuft mit `continue-on-error`, nichts blockiert Builds oder Merges.

| Werkzeug | Prüft |
|---|---|
| Bandit | Sicherheitsprobleme in Python (ab Schweregrad „mittel“) |
| pylint-odoo | Odoo-spezifische Regeln (Manifest, Felder, Views, Übersetzungen) |
| Ruff | allgemeine Python-Fehler (undefinierte Namen, unbenutzte Importe …) |
| gitleaks | Zugangsdaten/Secrets in der **gesamten Git-Historie** (Fundstellen werden im Log geschwärzt) |

Eingaben: `odoo-version` (Standard `19.0`), `python-version` (Standard `3.12`), `exclude-paths`
(kommagetrennt, z. B. Drittanbieter-Module, die nicht bewertet werden sollen).

**Ergebnis lesen:** Im Repo unter *Actions → Code-Scan → Lauf* steht oben eine Zusammenfassung
(Werkzeug, Anzahl Funde oder „keine Funde“). Ruff-Funde erscheinen zusätzlich als Anmerkungen an der Codezeile.

## Claude-Review (`claude-review.yml`)

- Läuft bei Pull Requests (`opened`, `synchronize`, `ready_for_review`, `reopened`), **Draft-PRs werden übersprungen**.
- Antwortet auf Kommentare mit `@claude` in Pull Requests.
- Reviewt auf Deutsch mit Fokus auf Sicherheit, Odoo-Best-Practices (19/20), Performance bei Recordset-Schleifen
  und Migrationsrisiken.
- Schreibt **nur Kommentare**; der Aufrufer vergibt `contents: read`, Claude kann nichts committen oder mergen.
- Benötigt das Secret `ANTHROPIC_API_KEY` (Organisations-Secret; im persönlichen Account je Repo) und die
  installierte Claude-GitHub-App.

## In ein Repo einbinden

Am einfachsten über die Vorlagen: *Actions → New workflow* im Repo, Abschnitt der Organisation
(„rivecon Code-Scan“, „rivecon Claude-Review“). Für Repos im persönlichen Account die Dateien aus
`workflow-templates/` nach `.github/workflows/` kopieren und `$default-branch` durch den Branch ersetzen.
Die `odoo-version` auf 19.0 oder 20.0 setzen.

## Odoo.sh-Kompatibilität

- Die Workflows laufen ausschließlich auf GitHub und haben **keinen Einfluss auf Odoo.sh-Builds**.
- Odoo.sh liefert den kompletten Git-Inhalt aus, also auch `.github/workflows/`. Das ist harmlos, wird aber
  mit auf die Instanz deployt.
- Nicht auf Produktions-Branches direkt pushen: Änderungen immer als Branch + Pull Request, Merge am besten
  mit dem nächsten regulären Deployment (ein Merge auf den Produktions-Branch löst bei Odoo.sh einen Build mit Neustart aus).
- Ein neuer Branch (z. B. `ci/rivecon-standard`) wird von Odoo.sh als Development-Branch erkannt und gebaut.
- Die Push-Trigger sind auf `main` und `stage` begrenzt (Pull Requests immer), damit `split/*`-Branches und
  Feature-Branches keine Actions-Minuten verbrauchen.
