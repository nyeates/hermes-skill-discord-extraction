# GitHub identity notes

## Commit author vs GitHub display user
GitHub can display a commit under an unexpected account even when the git author name looks correct.

### Durable rule
GitHub resolves commit attribution primarily from the commit email address. If the email is associated with a GitHub account, the web UI may show that account login/avatar even when the git author name is different.

## Practical guidance
- Setting `git config --global user.name` changes the commit author name.
- Setting `git config --global user.email` changes the commit email.
- If the goal is to avoid resolving to the wrong GitHub account, use the intended account's `users.noreply.github.com` address.

## Example pattern
If `gh api user` reports:
- `login`: `exampleuser`
- `id`: `123456`

then a safe noreply email is typically:
- `123456+exampleuser@users.noreply.github.com`

## Why this matters for this skill repo
This skill was moved into its own private GitHub repo. When testing future commits, check both:
1. local git author/committer (`git log -1 --format=...`), and
2. GitHub's displayed commit identity.

If those disagree, the issue is usually GitHub email mapping rather than local git config.