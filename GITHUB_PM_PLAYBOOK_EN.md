# GitHub Professional Project Template (AI-Ready)

**Purpose:** This document serves as both a human guide and an **AI execution template**.
**AI Instruction:** When asked to set up a project based on this file, execute the code blocks sequentially. Replace placeholders (like `<PROJECT_NAME>`, `<USER>`) with actual context.

---

## 🔑 AI Context & Variables
Before execution, define:
*   `$PROJECT_NAME`: (e.g., "my-app")
*   `$USER`: (e.g., "MarijanMiletic")
*   `$DESCRIPTION`: (e.g., "A new professional project")

---

## Phase 1: Initialization & Architecture
**Goal:** Create folder structure, git init, and remote repo.

```powershell
# 1. Setup Directories
mkdir $PROJECT_NAME
cd $PROJECT_NAME
New-Item -ItemType Directory -Force -Path src, tests, .github, .github/workflows, .github/ISSUE_TEMPLATE

# 2. Create Base Files
Set-Content -Path ".gitignore" -Value "src/__pycache__/`n*.pyc`n.env`nvenv/"
Set-Content -Path "README.md" -Value "# $PROJECT_NAME`n`n$DESCRIPTION"
Set-Content -Path "requirements.txt" -Value "# Deps"

# 3. Git Init & Push
git init
git add .
git commit -m "Chore: Initial commit"
gh repo create $PROJECT_NAME --public --source=. --remote=origin --push
```

## Phase 2: Project Management (V2)
**Goal:** Create Kanban board, link to repo, and setup roadmap fields.

```powershell
# 1. Create Project
$projectJson = gh project create --owner $USER --title "Roadmap" --format json | ConvertFrom-Json
$projectNumber = $projectJson.number
$projectId = $projectJson.id

# 2. Get Repo ID
$repoId = gh repo view "$USER/$PROJECT_NAME" --json id -q .id

# 3. LINK PROJECT TO REPO (GraphQL)
gh api graphql -f query='
  mutation($projectId: ID!, $repoId: ID!) {
    linkProjectV2ToRepository(input: { projectId: $projectId, repositoryId: $repoId }) {
      repository { name }
    }
  }' -f projectId=$projectId -f repoId=$repoId

# 4. Create Roadmap Fields
gh project field-create $projectNumber --owner $USER --name "Start Date" --data-type DATE
gh project field-create $projectNumber --owner $USER --name "Due Date" --data-type DATE
```

## Phase 3: Community Governance
**Goal:** Create standard health files in Root.

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

## Phase 4: Automation (CI/CD)
**Goal:** Setup GitHub Actions.

```yaml
# File: .github/workflows/ci.yml
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

## Phase 5: Advanced PM (Parent/Child Linking)
**Goal:** Link Sub-issues to Parent Issue using GraphQL.
**AI Note:** Use this exact mutation when user asks to "link tasks".

```powershell
# Variables: $ParentGlobalID (Issue ID), $ChildGlobalID (Issue ID)
gh api graphql -f query='
  mutation($issueId: ID!, $subIssueId: ID!) {
    addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) {
      issue { title }
    }
  }' -f issueId=$ParentGlobalID -f subIssueId=$ChildGlobalID
```

## Phase 6: Release
**Goal:** Create first release.

```powershell
gh release create v0.1.0 --title "Initial Release" --generate-notes
```
