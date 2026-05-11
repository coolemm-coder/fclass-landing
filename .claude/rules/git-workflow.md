# Git Workflow Rules

## Branch Strategy

```
main          - production ready code
├── feature/* - new features
├── fix/*     - bug fixes
└── hotfix/*  - urgent production fixes
```

## Commit Guidelines

### Commit Message Format
```
<type>: <short description>

[optional body]

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Types
- `feat:` - new feature
- `fix:` - bug fix
- `docs:` - documentation
- `refactor:` - code refactoring
- `style:` - CSS/design changes
- `chore:` - maintenance

### Examples
```
feat: add tour catalog pages for 6 countries

fix: resolve form submission error on mobile

style: update button colors to Sapphire Dreams palette
```

## Pre-Commit Checklist

- [ ] HTML validates (no W3C errors)
- [ ] No hardcoded secrets in code
- [ ] Tested on mobile viewport
- [ ] Forms submit correctly

## Pull Request Rules

### Title
Keep under 70 characters, use imperative mood:
- "Add Egypt tour page"
- "Fix contact form validation"

### Description Template
```markdown
## Summary
- Brief description of changes

## Test Plan
- [ ] Tested on Chrome
- [ ] Tested on Safari mobile
- [ ] Forms work correctly

## Screenshots (if UI change)
```

## Vercel Deploy

### Auto-deploy
- Push to `main` → auto-deploy to production
- Push to other branches → preview deployment

### Manual deploy
```bash
cd fclass-landing
npx vercel --prod --yes
```

## Protected Actions

### NEVER do without explicit request:
- `git push --force`
- `git reset --hard`
- Delete production files on Vercel

### ALWAYS verify before:
- Deploying to production
- Changing webhook URLs
- Modifying n8n workflows
