# Local demo runbook

## Start and inspect

From the repository root:

```bash
python3 -m demo.server
```

Open `http://127.0.0.1:8115`. Inspect `/api/health` for readiness. A port conflict can be resolved with `--port 8215`; keep the address local. The application prints its actual URL on startup.

## Data lifecycle

The first start creates `var/demo.sqlite3` and seeds synthetic records once. Closing the server or browser does not reset the data. An existing seed marker prevents accidental reseeding. Stop with Ctrl+C.

Use `--db var/review-02.sqlite3` to start a fresh review without destroying the previous workspace. For a backup, stop the process first and copy the database to another local path. Restart with `--db` pointing at that copy to inspect it. Never commit runtime databases; `var/` is ignored.

The `events` table retains every committed action. The UI intentionally shows only the most recent 12. SQL inspection can use any local SQLite client. No remote database or account is involved.

## Exports and reports

Use the header’s Export CSV link for the current runtime records. Run `make report` for the deterministic original baseline, which does not read or modify runtime state. Baseline reports are committed so reviewers can compare outputs.

## Verification

`make check` runs the Python suite, compiles source and checks both JavaScript modules. `npm ci`, `npx playwright install chromium`, then `npm run test:e2e` runs the isolated browser suite. The test server uses a separate port and a temporary database. Failure screenshots/traces go to ignored `test-results/`; GitHub Actions uploads them on failure.

## Troubleshooting

- **Workspace cannot load:** confirm the Python process is running, then open `/api/health` and reload.
- **Record changed:** another tab committed first. The browser refreshes the snapshot after HTTP 409; review the new state before resubmitting.
- **Business rule error:** the visible message explains the failed invariant. Validation failures keep form input available.
- **Port occupied:** use another `--port`. Do not stop unrelated processes.
- **Need a clean workspace:** choose a new `--db` path; preserve prior review data.
- **Missing browser binary:** run `npx playwright install chromium`. Linux CI uses `--with-deps`.

## Operating boundary

This is an unauthenticated local demonstration. Keep its loopback binding and use fictional records. Reservations and deliveries are simulated. No payment, real bakery order, routing optimisation, AI recommendation, real courier tracking, supplier integration or food-safety process is performed.
