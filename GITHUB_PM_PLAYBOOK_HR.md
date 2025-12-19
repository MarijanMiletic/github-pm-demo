# GitHub Project Management Priručnik (CLI Verzija)

Ovaj dokument opisuje kompletan proces postavljanja profesionalnog GitHub repozitorija s naprednim Project Management funkcijama koristeći GitHub CLI (`gh`).

## 1. Inicijalizacija Projekta
**Uloga:** Project Manager / Tech Lead

```bash
# Kreiraj mapu i osnovne datoteke
mkdir moj-projekt
cd moj-projekt
echo "# Moj Projekt" > README.md
echo "src/" > .gitignore

# Inicijaliziraj Git
git init
git add .
git commit -m "Inicijalni commit"

# Kreiraj i pošalji na GitHub
gh repo create moj-projekt --public --source=. --remote=origin --push
```

## 2. Postavljanje Projektne Ploče (Project Board V2)
**Uloga:** Project Manager

```bash
# Kreiraj Projekt
# Napomena: Ovo inicijalno kreira projekt na razini korisnika.
gh project create --owner <USERNAME> --title "Product Roadmap" --format json

# VAŽNO: Povezivanje Projekta s Repozitorijem
# (Zahtijeva GraphQL jer CLI to još ne podržava nativno)
# 1. Nabavi Project ID (Node ID, počinje s PVT_...)
# 2. Nabavi Repo ID (Node ID, počinje s R_...)
# 3. Pokreni Mutaciju:
gh api graphql -f query=' 
  mutation($projectId: ID!, $repoId: ID!) {
    linkProjectV2ToRepository(input: { projectId: $projectId, repositoryId: $repoId }) {
      repository { name }
    }
  }' -f projectId="<PROJECT_ID>" -f repoId="<REPO_ID>"
```

## 3. Planiranje i Roadmapping
**Uloga:** Project Manager

### Kreiranje Milestones (Sprintova)
```bash
gh api repos/<OWNER>/<REPO>/milestones -f title="Sprint 1" -f due_on="2025-12-30T17:00:00Z"
```

### Kreiranje Custom Polja (Datumi)

```bash
# Dodaj Start Date i Due Date za Timeline prikaz (Roadmap)
gh project field-create <PROJECT_NUMBER> --owner <USERNAME> --name "Start Date" --data-type DATE
gh project field-create <PROJECT_NUMBER> --owner <USERNAME> --name "Due Date" --data-type DATE
```

## 4. Upravljanje Zadacima (Task Management)

### A. Glavni Zadatak (Parent Issue / User Story)
**Uloga:** Project Manager
**Fokus:** ŠTO i ZAŠTO.
```bash
gh issue create --title "Funkcionalnost prijave korisnika" \
                --body "Kao korisnik, želim se prijaviti da vidim svoje podatke." \
                --label "enhancement" \
                --milestone "Sprint 1" \
                --assignee "@me"
# (Pretpostavimo da je ovo Issue #5)
```

### B. Pod-zadaci (Sub-issues / Technical Tasks)
**Uloga:** Developeri (tijekom planiranja)
**Fokus:** KAKO.
```bash
# Kreiranje tehničkih zadataka
gh issue create --title "Impl: OAuth2 Klijent" --body "Tehnički detalji..." --label "devops"
gh issue create --title "Impl: Login Forma UI" --body "Tehnički detalji..." --label "frontend"
# (Pretpostavimo da su ovo Issues #9, #10)
```

### C. Povezivanje Roditelja i Djece (Sub-issue Magija)
**Uloga:** Project Manager / Lead
**Metoda:** GraphQL Mutacija (addSubIssue)
```bash
# Poveži Issue #9 kao dijete Issue-a #5
gh api graphql -f query=' 
  mutation($issueId: ID!, $subIssueId: ID!) {
    addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
      issue { title }
    }
  }' -f issueId="<PARENT_GLOBAL_ID>" -f subIssueId="<CHILD_GLOBAL_ID>"
```

## 5. Razvojni Proces (Workflow)
**Uloga:** Developer

1.  **Odaberi zadatak:** Pomakni u "In Progress" na ploči.
2.  **Nova grana:** `git checkout -b feature/login-auth`
3.  **Kodiranje i testiranje.**
4.  **Slanje koda:** `git push -u origin feature/login-auth`
5.  **Pull Request:**
    ```bash
    gh pr create --title "Feat: Login Auth" --body "Closes #9, Closes #10"
    ```

## 6. Automatizacija i Upravljanje (DevOps)

### CI/CD Pipeline (GitHub Actions)
Kreiraj datoteku `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m unittest discover
```

### Standardizacija (Templates)
Kreiraj sljedeće mape i datoteke za profesionalni izgled:
```bash
mkdir .github/ISSUE_TEMPLATE
# Kreiraj .github/ISSUE_TEMPLATE/bug_report.md
# Kreiraj .github/ISSUE_TEMPLATE/feature_request.md
# Kreiraj .github/pull_request_template.md
# Kreiraj .github/CODEOWNERS
# Kreiraj SECURITY.md
```

### Zaštita Grana (Branch Protection)
**Uloga:** Project Manager
Zabrani direktno slanje koda na master granu.
```bash
gh api repos/<OWNER>/<REPO>/branches/master/protection -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null
```

## 7. Upravljanje Verzijama (Releases)
**Uloga:** Lead / PM
Kada je Sprint gotov i CI prolazi.
```bash
gh release create v1.0.0 --title "v1.0.0 - MVP" --notes "Prva produkcijska verzija."
```
