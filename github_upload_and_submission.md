# GitHub Creation And Challenge Submission

## Repository Status

The intended new public repository is `https://github.com/silambarasanc199-jpg/GlucoTwin-AI-2.0`. It was not created or pushed by this project bundle because an authenticated GitHub session was unavailable. An unauthenticated request to the URL showed GitHub's not-found page; that cannot distinguish a nonexistent repository from a private one. Check with authenticated GitHub CLI access before creating anything.

The existing public repository `https://github.com/silambarasanc199-jpg/Glucotwin-ai` was inspected only and was not modified. Do not fork, rename, or push this work to it.

## Safe Creation And Push

Download and extract the project ZIP, open a terminal in the extracted `GlucoTwin-AI-2.0` folder, and run the following commands. GitHub CLI (`gh`) must be installed and authenticated as `silambarasanc199-jpg`; authentication uses the CLI's secure login flow, not a token pasted into a command.

```bash
gh auth status
gh repo view silambarasanc199-jpg/GlucoTwin-AI-2.0 --json nameWithOwner,url,isPrivate,defaultBranchRef
```

If `gh repo view` succeeds, stop and inspect that repository and its commit history. Preserve it; do not initialize a replacement or push this project over it. If it fails because authentication is missing or the account lacks access, stop and resolve access first. Only proceed when the authenticated check confirms no repository exists under that account.

After confirming the repository does not exist, initialize the extracted project and inspect the files before staging:

```bash
git init -b main
git status --short --ignored
```

If Git asks for an author identity, configure it locally for this repository using a name and email you choose. Stage only the reviewed project files; this deliberately avoids local databases, generated data/model binaries, virtual environments, and caches:

```bash
git add .gitignore .env.example .github LICENSE README.md app data/README.md docs models/README.md models/evaluation.json pytest.ini requirements.txt run.py tests tools
git status --short
git diff --cached --stat
git diff --cached --name-only
```

Confirm the staged list contains no `.env`, patient data, local SQLite database, `.venv`, cache, or model binary. Then commit and create/push the new public repository:

```bash
git commit -m "Build GlucoTwin AI digital twin prototype"
gh repo create silambarasanc199-jpg/GlucoTwin-AI-2.0 --public --source=. --remote=origin --push
```

This last command creates a public repository and publishes the staged project. Verify the resulting remote and uploaded branch without force-pushing:

```bash
git remote -v
git ls-remote --heads origin main
gh repo view silambarasanc199-jpg/GlucoTwin-AI-2.0 --json nameWithOwner,url,isPrivate,defaultBranchRef
```

Confirm the repository is public in a signed-out browser, open the README, and inspect `app/`, `tests/`, `models/evaluation.json`, and `docs/`. Never use `--force` or overwrite an existing repository history.

## Official Challenge Requirements

The live [Happiest Health Digital Twin Challenge 2026 page on Unstop](https://unstop.com/hackathons/crp-digital-twin-challenge-2026-happiest-health-1757873) was checked on 20 October 2026. It specifies a team of 1–4 full-time students, fusion of historical/simulated EHR context and synthetic/open-source wearable time-series, prediction of a specific adverse event, a conceptual dashboard, a public GitHub repository, README team/project/technical details, an open-source license, architecture diagram in PDF/PPT, a project presentation in PDF/PPT, and a **minimum 20-minute** explanatory prototype video. Recheck the page before submitting because challenge pages can change.

## Final Checklist

- [ ] Confirm full-time student eligibility and the registered team (1–4 students); verify names and college/incubator information with the team.
- [ ] Create the new public repository only after an authenticated check confirms the name is not already in use; keep `Glucotwin-ai` untouched.
- [ ] Add the verified repository URL to the competition form only after the public page, README, branch, commit, and files have been checked.
- [ ] Review team, mentor, and contact details in the README; submit the team leader's name, phone, email, and public repository link through the official platform.
- [ ] Run generation, training, evaluation, setup, and tests from a clean environment; check the current metrics against `models/evaluation.json`.
- [ ] Start the app, confirm `/health` and `/docs`, inspect a clearly synthetic profile, and exercise reading entry and prediction.
- [ ] Record a real video of at least 20 minutes using `docs/demo_script.md`; review it, upload it as permitted, verify the link plays, and replace the README's video status with the actual link.
- [ ] Recheck presentation and architecture PDFs/PPTX, public repository access, and all README links before submitting.
- [ ] Do not claim clinical validation, a real-time wearable connection, a deployment, a recorded video, or competition results unless separately verified.
