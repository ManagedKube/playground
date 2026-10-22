# Nellis Auction – Place Bid (TypeScript)

Automates logging in to [nellisauction.com](https://www.nellisauction.com),
searching for an item, and placing a bid – all from a GitHub Actions workflow.

## Features

- **Session persistence** – cookies are saved to `cookies.json` after login so
  the next run can reuse the session without logging in again.
- **Two-factor authentication** – the site may send a 6-digit SMS code.  Pass
  the code via the `NELLIS_2FA_CODE` environment variable or the
  `two_factor_code` workflow dispatch input.
- **TypeScript** with unit tests (Jest) and an e2e test script.

## How to give the GHA the 2FA code

The GitHub Actions workflow is configured with
[`workflow_dispatch`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch)
and accepts a `two_factor_code` input.  When the SMS arrives on your phone:

1. Go to **Actions → Nellis – Place Bid → Run workflow**.
2. Fill in the **Two-factor code** field.
3. Click **Run workflow**.

The code is passed to the script as the `NELLIS_2FA_CODE` environment variable.

## Environment variables / secrets

| Name                  | Required | Description                                     |
|-----------------------|----------|-------------------------------------------------|
| `NELLIS_EMAIL`        | yes      | Your nellisauction.com account e-mail           |
| `NELLIS_PASSWORD`     | yes      | Your account password                           |
| `NELLIS_2FA_CODE`     | no\*     | 6-digit SMS code (\* required when 2FA fires)   |
| `NELLIS_COOKIE_FILE`  | no       | Path to persist cookies (default: `cookies.json`) |

Store `NELLIS_EMAIL` and `NELLIS_PASSWORD` as
[GitHub Actions secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets).

## Local development

```bash
cd nellisauction.com/place_bid_ts
npm install

# Run unit tests
npm test

# Run e2e login test (requires real credentials)
NELLIS_EMAIL=you@example.com NELLIS_PASSWORD=secret npm run test:e2e

# Build and run
npm run build
NELLIS_EMAIL=... NELLIS_PASSWORD=... node dist/index.js "laptop" 50
```

## Usage

```
NELLIS_EMAIL=<email> NELLIS_PASSWORD=<pass> [NELLIS_2FA_CODE=<code>] \
  node dist/index.js "<search query>" [bidAmount]
```

- **search query** – text to search for on Nellis (e.g. `"laptop"`)
- **bidAmount** – maximum bid in USD (default: `1`)
