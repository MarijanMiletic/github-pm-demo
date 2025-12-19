# GitHub Project Management Playbook (CLI Edition)

This guide documents the complete workflow for setting up a professional GitHub repository with advanced Project Management features using the GitHub CLI (`gh`).

## 1. Project Initialization
**Role:** Project Manager / Tech Lead

```bash
# Create directory and basic files
mkdir my-project
cd my-project
echo "# My Project" > README.md
echo "src/" > .gitignore

# Initialize Git
git init
git add .
git commit -m "Initial commit"

# Create and push to GitHub
gh repo create my-project --public --source=. --remote=origin --push
```

## 2. Project Board Setup (V2)
**Role:** Project Manager

```bash
# Create the Project Board
# Note: This creates a User-level project initially.
gh project create --owner <USERNAME> --title "Product Roadmap" --format json

# CRITICAL: Link Project to Repository
# (Requires GraphQL because CLI doesn't support this natively yet)
# 1. Get Project ID (Node ID, starts with PVT_...)
# 2. Get Repo ID (Node ID, starts with R_...)
# 3. Run Mutation:
gh api graphql -f query=' 
  mutation($projectId: ID!, $repoId: ID!) { 
    linkProjectV2ToRepository(input: { projectId: $projectId, repositoryId: $repoId }) { 
      repository { name } 
    } 
  }' -f projectId="<PROJECT_ID>" -f repoId="<REPO_ID>"
```

## 3. Roadmapping & Planning
**Role:** Project Manager

### Creating Milestones (Sprints)
```bash
gh api repos/<OWNER>/<REPO>/milestones -f title="Sprint 1" -f due_on="2025-12-30T17:00:00Z"
```

### Creating Custom Fields (Dates)
```bash
# Add Start Date and Due Date for Timeline View
gh project field-create <PROJECT_NUMBER> --owner <USERNAME> --name "Start Date" --data-type DATE
gh project field-create <PROJECT_NUMBER> --owner <USERNAME> --name "Due Date" --data-type DATE
```

## 4. Task Management Workflow

### A. The Parent Issue (User Story)
**Role:** Project Manager
**Focus:** WHAT and WHY.
```bash
gh issue create --title "User Login Feature" \
                --body "As a user, I want to log in so I can access my data." \
                --label "enhancement" \
                --milestone "Sprint 1" \
                --assignee "@me"
# (Assume this creates Issue #5)
```

### B. The Sub-issues (Technical Tasks)
**Role:** Developers (during Planning)
**Focus:** HOW.
```bash
# Create technical tasks
gh issue create --title "Impl: OAuth2 Client" --body "Tech details..." --label "devops"
gh issue create --title "Impl: Login Form UI" --body "Tech details..." --label "frontend"
# (Assume these are Issues #9, #10)
```

### C. Linking Parent & Child (The "Sub-issue" Magic)
**Role:** Project Manager / Lead
**Method:** GraphQL Mutation (addSubIssue)
```bash
# Link Issue #9 as a child of Issue #5
gh api graphql -f query=' 
  mutation($issueId: ID!, $subIssueId: ID!) { 
    addSubIssue(input: { issueId: $issueId, subIssueId: $subIssueId }) { 
      issue { title } 
    } 
  }' -f issueId="<PARENT_GLOBAL_ID>" -f subIssueId="<CHILD_GLOBAL_ID>"
```

## 5. Development Workflow
**Role:** Developer

1.  **Pick a task:** Move to "In Progress" on Board.
2.  **Branch:** `git checkout -b feature/login-auth`
3.  **Code & Test.**
4.  **Push:** `git push -u origin feature/login-auth`
5.  **Pull Request:**
    ```bash
    gh pr create --title "Feat: Login Auth" --body "Closes #9, Closes #10"
    ```

## 6. Automation & Governance (DevOps)

### CI/CD Pipeline (GitHub Actions)
Create `.github/workflows/ci.yml`:
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

### Templates & Standards
Run these to set up governance files:
```bash
mkdir .github/ISSUE_TEMPLATE
# Create .github/ISSUE_TEMPLATE/bug_report.md
# Create .github/ISSUE_TEMPLATE/feature_request.md
# Create .github/pull_request_template.md
# Create .github/CODEOWNERS
# Create SECURITY.md
```

### Branch Protection
**Role:** Project Manager
Prevent direct pushes to master.
```bash
gh api repos/<OWNER>/<REPO>/branches/master/protection -X PUT \
  -f required_status_checks='{"strict":true,"contexts":["test"]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}' \
  -f restrictions=null
```

## 7. Release Management
**Role:** Lead / PM
When Sprint is done and CI is green.
```bash
gh release create v1.0.0 --title "v1.0.0 - MVP" --notes "First production release."
```

