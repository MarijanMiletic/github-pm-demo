# GitHub Project Management & Engineering Playbook

This guide documents the complete workflow for setting up and managing a professional-grade GitHub repository using the GitHub CLI (`gh`).

---

## 1. Project Initialization & Architecture
**Role:** Tech Lead / Architect

```bash
# Setup project structure
mkdir my-project && cd my-project
echo "src/" > .gitignore
echo "tests/" >> .gitignore
echo "# My Professional Project" > README.md

# Initialize and push
git init && git add . && git commit -m "Chore: Project initialization"
gh repo create my-project --public --source=. --remote=origin --push
```

## 2. Advanced Project Planning (V2 Projects)
**Role:** Senior Project Manager

### Setup & Linking
```bash
# Create the board
gh project create --owner <USER> --title "Strategic Roadmap" --format json

# LINK PROJECT TO REPO (Crucial for visibility)
# Use GraphQL to link Project ID (PVT_...) and Repo ID (R_...)
gh api graphql -f query='\n  mutation($projectId: ID!, $repoId: ID!) {\n    linkProjectV2ToRepository(input: { projectId: $projectId, repositoryId: $repoId }) {\n      repository { name }\n    }\n  }\\n' -f projectId="<PROJ_ID>" -f repoId="<REPO_ID>"
```

### Visualizing Progress (Roadmap)
```bash
# Create Date fields for Timeline/Roadmap view
gh project field-create <PROJ_NUM> --owner <USER> --name "Start Date" --data-type DATE
gh project field-create <PROJ_NUM> --owner <USER> --name "Due Date" --data-type DATE
```

## 3. Community Standards & Governance
**Role:** Compliance / Project Manager
*These files ensure your project meets the "GitHub Community Standards".*

```bash
# Create Governance Files in Root
# 1. LICENSE (MIT)
# 2. CODE_OF_CONDUCT.md
# 3. CONTRIBUTING.md
# 4. SECURITY.md
# 5. SUPPORT.md
# 6. AUTHORS & CHANGELOG.md

# Setup Templates (Automation for human input)
mkdir -p .github/ISSUE_TEMPLATE
# Create bug_report.md and feature_request.md inside
# Create .github/pull_request_template.md
```

## 4. Professional Task Workflow

### A. Parent Issue (Strategy)
```bash
gh issue create --title "Feat: User Authentication" \
                --body "As a user, I want to secure my account." \
                --milestone "Sprint 1" --label "enhancement"
```

### B. Sub-Issues (Tactics)
```bash
gh issue create --title "Auth: Database Schema" --label "devops"
gh issue create --title "Auth: API Endpoints" --label "backend"
```

### C. Native Hierarchy (Parent/Child Linking)
```bash
# Link Issue #9 (Child) to Issue #5 (Parent)
gh api graphql -f query='\n  mutation($issueId: ID!, $subIssueId: ID!) {\n    addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {\n      issue { title }\n    }\n  }\\n' -f issueId="<PARENT_GLOBAL_ID>" -f subIssueId="<CHILD_GLOBAL_ID>"
```

## 5. Engineering & CI/CD
**Role:** DevOps / Developer

### GitHub Actions (Continuous Integration)
Create `.github/workflows/ci.yml` to automate testing:
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

### Branch Protection (Enforcing Laws)
```bash
# Prevent direct pushes and require passing CI
gh api repos/<OWNER>/<REPO>/branches/master/protection -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}'
```

## 6. Release Management
**Role:** Release Manager
```bash
# Create a formal release with auto-generated notes
gh release create v1.0.0 --title "v1.0.0 Stable" --generate-notes
```

---
**Summary Checklist:**
- [ ] README.md with Badges
- [ ] LICENSE / CODE_OF_CONDUCT / CONTRIBUTING in Root
- [ ] .github/ (Templates & Workflows)
- [ ] Project Linked to Repo
- [ ] Branch Protection Active

```