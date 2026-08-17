# OTIS Opportunity Tracker

Private static tracker plus scheduled GitHub Actions scanner for public SOF/SOCOM/DIU opportunities.

## What it does
- Hosts a browser tracker with deadline, fit, urgency, sponsor, and status fields.
- Imports and exports normalized tracker JSON.
- Keeps canonical records in `data/opportunities.json`.
- Runs a dependency-free daily scan at 13:00 UTC.
- Writes source reports and keyword-matched candidates to `reports/`.

The scanner reads public pages only. It does not submit material or make bid/no-bid decisions. Review `reports/candidates.json`, then promote validated records to `data/opportunities.json`.

## Deploy
Connect `SkyGuardDefense/otis-tracker` to Netlify. Use no build command and publish directory `.`; `netlify.toml` supplies this setting. To replace the current tracker, connect this repository to the existing Netlify site.

## Runner
The workflow runs daily at 13:00 UTC and can be manually dispatched in GitHub Actions. It has `contents: write` permission to commit scan artifacts. GitHub may delay scheduled jobs; manually dispatch for time-sensitive checks. No secret is required for the public-page scanner. Add any future credentials only as GitHub Actions secrets.

## Record format
```json
{"id":"diu-example-001","opportunity":"Official title","sponsor":"DIU","channel":"DIU Open Solicitation","sourceUrl":"https://example.mil/","datePosted":"2026-08-17","deadline":"2026-08-28","awardType":"Commercial Solutions Opening","otisMatch":["EO/IR","Sensor Fusion"],"fitScore":5,"urgency":"ESCALATE","status":"Open","nextAction":"Review solicitation and make bid/no-bid decision","lastChecked":"2026-08-17T13:00:00Z"}
```
Use `ESCALATE` for verified deadlines within 14 days; do not infer deadlines from announcements.
