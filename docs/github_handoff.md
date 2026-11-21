# GitHub handoff

## Current local history

- `main` records the attributed model-double checkpoint.
- `setup/project-foundation` adds the finalized scope, target architecture,
  setup diagnostic and CI configuration.
- No commit is attributed to the learner. Their first independent change is
  still the `learning/top-k` exercise.
- `feature/fullstack-integration` combines the catalogue and foundation at checkpoint 0C.
- On 21 November 2026, the connected GitHub account was verified as `rachitagundi`.
  No EnergyAtlas repository appeared in the accessible repository list. The connector
  cannot create repositories, the CLI is unauthenticated, and the browser requires
  GitHub sign-in. No hosted repository, push or pull request has been completed.

## Resume after GitHub is connected

1. Follow the connected GitHub integration's instructions and verify the actual
   signed-in account. Do not guess the GitHub username from a person's name.
2. Check whether `EnergyAtlas` already exists. Inspect any matching repository
   before reusing it; preserve existing user work and avoid duplicate creation.
3. Create an empty **private** repository if needed. Do not generate another
   README or overwrite an existing repository. Use its returned clone URL.
4. Add the verified remote, push `main` first, and then push
   `setup/project-foundation` and `feature/fullstack-integration`. Keep `main` as the default branch.
5. Open a **draft pull request** from the foundation branch into `main`, using
   [the prepared description](pull_requests/project-foundation.md).
6. Inspect the actual Ubuntu and Windows workflow results. Configuration in a
   file is not evidence that a hosted run passed. Fix failures before merging.
7. Review the pull request with the learner, merge it, and start their independent
   `learning/top-k` branch from the updated main branch.

Do not request tokens in chat. Use the GitHub connection or the user's own
authenticated GitHub CLI. Public portfolio publication follows the completed
demo and the source/contribution review.

## Optional restore from the repository backup

The backup ZIP includes the working source folder and a separate Git bundle.
From the extracted ZIP's top-level directory, PowerShell can restore the integrated branch:

```powershell
git clone -b feature/fullstack-integration .\EnergyAtlas_history.bundle EnergyAtlas-git
```

The clone's `origin` initially points to the local bundle, not GitHub. Update it
to the verified GitHub URL when the hosted repository is ready. Configure your
own commit identity locally before making your independent change. The backup
contains mentor-authored commits, not credentials or user-attributed commits.
