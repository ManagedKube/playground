/**
 * index.ts – CLI entry point
 *
 * Usage:
 *   NELLIS_EMAIL=... NELLIS_PASSWORD=... [NELLIS_2FA_CODE=...] \
 *     node dist/index.js "search query" [bidAmount]
 *
 * Environment variables:
 *   NELLIS_EMAIL        – account e-mail (required)
 *   NELLIS_PASSWORD     – account password (required)
 *   NELLIS_2FA_CODE     – 6-digit SMS code (required when 2FA is triggered)
 *   NELLIS_COOKIE_FILE  – path to session cookie file (default: ./cookies.json)
 *
 * Arguments:
 *   argv[2]  – search query string (required)
 *   argv[3]  – maximum bid amount in USD (optional, default: 1)
 */

import { login } from './login';
import { searchItems, placeBid } from './placeBid';

async function main(): Promise<void> {
  const email = process.env['NELLIS_EMAIL'];
  const password = process.env['NELLIS_PASSWORD'];
  const twoFactorCode = process.env['NELLIS_2FA_CODE'];
  const cookieFile = process.env['NELLIS_COOKIE_FILE'];

  if (!email || !password) {
    console.error('Error: NELLIS_EMAIL and NELLIS_PASSWORD must be set.');
    process.exit(1);
  }

  const query = process.argv[2];
  if (!query) {
    console.error('Usage: node dist/index.js "<search query>" [bidAmount]');
    process.exit(1);
  }

  const bidAmount = process.argv[3] ? parseInt(process.argv[3], 10) : 1;

  // ── Login ──────────────────────────────────────────────────────────────────
  console.log(`Logging in as ${email}…`);
  const loginResult = await login({ email, password, twoFactorCode, cookieFile });

  if (!loginResult.success) {
    if (loginResult.needsTwoFactor) {
      console.error(
        'Two-factor authentication required.\n' +
          'Re-run with NELLIS_2FA_CODE=<code> set to the SMS code sent to your phone.'
      );
    } else {
      console.error(`Login failed: ${loginResult.message}`);
    }
    process.exit(2);
  }

  console.log(loginResult.message);

  // ── Search ─────────────────────────────────────────────────────────────────
  console.log(`Searching for: "${query}"…`);
  const results = await searchItems(loginResult.client, query);

  if (results.length === 0) {
    console.log('No items found. Nothing to bid on.');
    process.exit(0);
  }

  console.log(`Found ${results.length} item(s). First result:`);
  const first = results[0]!;
  console.log(`  ID:          ${first.productId}`);
  console.log(`  Title:       ${first.title}`);
  console.log(`  Current bid: $${first.currentBid}`);
  console.log(`  URL:         ${first.url}`);

  // ── Place bid ──────────────────────────────────────────────────────────────
  console.log(`Placing bid of $${bidAmount} on product ${first.productId}…`);
  const bidResult = await placeBid(loginResult.client, {
    productId: first.productId,
    bidAmount,
  });

  if (bidResult.success) {
    console.log(`✓ ${bidResult.message}`);
  } else {
    console.error(`✗ ${bidResult.message}`);
    process.exit(3);
  }
}

main().catch((err: unknown) => {
  console.error('Unexpected error:', err);
  process.exit(1);
});
