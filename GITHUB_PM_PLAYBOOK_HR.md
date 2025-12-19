# GitHub Profesionalni Projektni Predložak (AI-Spreman)

**Svrha:** Ovaj dokument služi kao vodič za ljude i **predložak za izvršavanje za AI**.
**AI Uputa:** Kada dobiješ zadatak postaviti projekt prema ovom dokumentu, izvršavaj blokove koda sekvencijalno. Zamijeni varijable (npr. `$PROJECT_NAME`, `$USER`) stvarnim podacima.

---

## 🔑 AI Kontekst & Varijable
Prije izvršavanja definiraj:
*   `$PROJECT_NAME`: (npr. "moj-projekt")
*   `$USER`: (npr. "MarijanMiletic")
*   `$DESCRIPTION`: (npr. "Opis projekta...")

---

## Faza 1: Inicijalizacija & Arhitektura
**Cilj:** Struktura mapa, git init, remote repo.

```powershell
# 1. Postavi Mape
mkdir $PROJECT_NAME
cd $PROJECT_NAME
New-Item -ItemType Directory -Force -Path src, tests, .github, .github/workflows, .github/ISSUE_TEMPLATE

# 2. Kreiraj Bazne Datoteke
Set-Content -Path ".gitignore" -Value "src/__pycache__/`n*.pyc`n.env`nvenv/"
Set-Content -Path "README.md" -Value "# $PROJECT_NAME`n`n$DESCRIPTION"
Set-Content -Path "requirements.txt" -Value "# Deps"

# 3. Git Init & Push
git init
git add .
git commit -m "Chore: Inicijalni commit"
gh repo create $PROJECT_NAME --public --source=. --remote=origin --push
```

## Faza 2: Project Management (V2)
**Cilj:** Kanban ploča, povezivanje s repoom, roadmap polja.

```powershell
# 1. Kreiraj Projekt
$projectJson = gh project create --owner $USER --title "Roadmap" --format json | ConvertFrom-Json
$projectNumber = $projectJson.number
$projectId = $projectJson.id

# 2. Dohvati Repo ID
$repoId = gh repo view "$USER/$PROJECT_NAME" --json id -q .id

# 3. POVEŽI PROJEKT S REPOOM (GraphQL)
gh api graphql -f query='
  mutation($projectId: ID!, $repoId: ID!) {
    linkProjectV2ToRepository(input: { projectId: $projectId, repositoryId: $repoId }) {
      repository { name }
    }
  }' -f projectId=$projectId -f repoId=$repoId

# 4. Kreiraj polja za Roadmap
gh project field-create $projectNumber --owner $USER --name "Start Date" --data-type DATE
gh project field-create $projectNumber --owner $USER --name "Due Date" --data-type DATE
```

## Faza 3: Community Governance
**Cilj:** Kreirati standardne datoteke u Rootu.

```powershell
# LICENSE (MIT)
Set-Content -Path "LICENSE" -Value "MIT License`nCopyright (c) 2025 $USER..."

# CODE_OF_CONDUCT (Contributor Covenant)
Set-Content -Path "CODE_OF_CONDUCT.md" -Value "# Contributor Covenant Code of Conduct..."

# CONTRIBUTING
Set-Content -Path "CONTRIBUTING.md" -Value "# Contributing`n1. Fork`n2. PR..."

# SECURITY & SUPPORT
Set-Content -Path "SECURITY.md" -Value "# Security Policy..."
Set-Content -Path "SUPPORT.md" -Value "# Support..."
```

## Faza 4: Automatizacija (CI/CD)
**Cilj:** Postaviti GitHub Actions.

```yaml
# Datoteka: .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m unittest discover tests
```

## Faza 5: Napredni PM (Parent/Child Povezivanje)
**Cilj:** Povezati Sub-issues s Parent Issue koristeći GraphQL.
**AI Napomena:** Koristi točno ovu mutaciju kada korisnik traži "linkanje taskova".

```powershell
# Varijable: $ParentGlobalID (Issue ID), $ChildGlobalID (Issue ID)
gh api graphql -f query='
  mutation($issueId: ID!, $subIssueId: ID!) {
    addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
      issue { title }
    }
  }' -f issueId=$ParentGlobalID -f subIssueId=$ChildGlobalID
```

## Faza 6: Release
**Cilj:** Kreirati prvu verziju.

```powershell
gh release create v0.1.0 --title "Inicijalna Verzija" --generate-notes
```
