# GitHub Priručnik za Upravljanje Projektima i Inženjerstvo

Ovaj priručnik dokumentira potpuni proces postavljanja i vođenja profesionalnog GitHub repozitorija koristeći GitHub CLI (`gh`).

---

## 1. Inicijalizacija i Arhitektura
**Uloga:** Tech Lead / Arhitekt

```bash
# Postavljanje strukture
mkdir moj-projekt && cd moj-projekt
echo "src/" > .gitignore
echo "tests/" >> .gitignore
echo "# Moj Profesionalni Projekt" > README.md

# Git inicijalizacija
git init && git add . && git commit -m "Chore: Inicijalizacija projekta"
gh repo create moj-projekt --public --source=. --remote=origin --push
```

## 2. Napredno Planiranje (V2 Projekti)
**Uloga:** Senior Project Manager

### Postavljanje i Povezivanje
```bash
# Kreiraj projektnu ploču (Kanban)
gh project create --owner <USER> --title "Strateški Plan" --format json

# POVEŽI PROJEKT S REPOZITORIJEM (Ključno za vidljivost)
# Koristi GraphQL za povezivanje Project ID-a (PVT_...) i Repo ID-a (R_...)
gh api graphql -f query=' 
  mutation($projectId: ID!, $repoId: ID!) { 
    linkProjectV2ToRepository(input: { projectId: $projectId, repositoryId: $repoId }) { 
      repository { name } 
    } 
  }' -f projectId="<PROJ_ID>" -f repoId="<REPO_ID>"
```

### Vizualizacija (Roadmap/Vremenska crta)
```bash
# Kreiraj datumska polja za Roadmap prikaz
gh project field-create <PROJ_NUM> --owner <USER> --name "Start Date" --data-type DATE
gh project field-create <PROJ_NUM> --owner <USER> --name "Due Date" --data-type DATE
```

## 3. Standardi Zajednice i Upravljanje (Governance)
**Uloga:** Compliance / Project Manager
*Ove datoteke osiguravaju da projekt zadovoljava "GitHub Community Standards".*

```bash
# Kreiraj ključne datoteke u korijenu (Root)
# 1. LICENSE (MIT) - Pravna zaštita
# 2. CODE_OF_CONDUCT.md - Pravila ponašanja
# 3. CONTRIBUTING.md - Upute za suradnike
# 4. SECURITY.md - Sigurnosna politika
# 5. SUPPORT.md - Upute za pomoć
# 6. AUTHORS & CHANGELOG.md - Povijest i zasluge

# Postavljanje Predložaka (Automatizacija unosa)
mkdir -p .github/ISSUE_TEMPLATE
# Kreiraj bug_report.md i feature_request.md unutar mape
# Kreiraj .github/pull_request_template.md za PR-ove
```

## 4. Profesionalni Proces Zadataka

### A. Roditeljski Zadatak (Strategija)
```bash
gh issue create --title "Feat: Autentifikacija korisnika" \
                --body "Kao korisnik, želim osigurati svoj račun." \
                --milestone "Sprint 1" --label "enhancement"
```

### B. Pod-zadaci (Tehnička provedba)
```bash
gh issue create --title "Auth: Shema baze podataka" --label "devops"
gh issue create --title "Auth: API Endpoints" --label "backend"
```

### C. Hijerarhija (Povezivanje Parent/Child)
```bash
# Poveži Issue #9 (Dijete) s Issue-om #5 (Roditelj)
gh api graphql -f query=' 
  mutation($issueId: ID!, $subIssueId: ID!) { 
    addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) { 
      issue { title } 
    } 
  }' -f issueId="<PARENT_GLOBAL_ID>" -f subIssueId="<CHILD_GLOBAL_ID>"
```

## 5. Inženjerstvo i CI/CD
**Uloga:** DevOps / Developer

### GitHub Actions (Kontinuirana Integracija)
Kreiraj `.github/workflows/ci.yml` za automatsko testiranje:
```yaml
name: Python CI
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

### Zaštita Grana (Zabrana push-a na master)
```bash
# Zabrani direktne push-eve i zahtijevaj prolazak testova
gh api repos/<OWNER>/<REPO>/branches/master/protection -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}'
```

## 6. Upravljanje Verzijama (Releases)
**Uloga:** Release Manager
```bash
# Kreiraj službenu verziju s automatskim bilješkama
gh release create v1.0.0 --title "v1.0.0 Stable" --generate-notes
```

---
**Završna Checklista:**
- [ ] README.md s Badges (značkama)
- [ ] LICENSE / CODE_OF_CONDUCT / CONTRIBUTING u Rootu
- [ ] .github/ mapa spremna (Predlošci & Workflows)
- [ ] Projektna ploča povezana s repozitorijem
- [ ] Zaštita grana aktivna