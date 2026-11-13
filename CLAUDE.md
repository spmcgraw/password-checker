# password-checker

CLI that checks Proton Pass vault passwords against Have I Been Pwned (k-anonymity).

## Working conventions

- **Branch from `main` before starting any work.** Never commit directly to `main`.
  Start each piece of work with `git switch main && git pull && git switch -c <branch>`.
- **Name branches with a type prefix**: `feature/`, `chore/`, `bug/` (also `fix/`,
  `docs/`, `refactor/`), followed by a short kebab-case description, e.g.
  `feature/close-checklist`, `bug/duplicate-entries`, `chore/deps-bump`.
- Work in the main checkout, not a git worktree.
