/**
 * e2e/login.e2e.ts
 *
 * End-to-end test for logging in to nellisauction.com.
 *
 * These tests make real HTTP requests. They require the following
 * environment variables to be set:
 *
 *   NELLIS_EMAIL        – your account e-mail address
 *   NELLIS_PASSWORD     – your account password
 *   NELLIS_2FA_CODE     – SMS code (only needed when 2FA is triggered)
 *   NELLIS_COOKIE_FILE  – (optional) path to store session cookies
 *
 * Run:
 *   NELLIS_EMAIL=... NELLIS_PASSWORD=... npx ts-node e2e/login.e2e.ts
 *
 * Or via npm:
 *   npm run test:e2e
 */

import { login } from '../src/login';

async function runE2ELogin(): Promise<void> {
  const email = process.env['NELLIS_EMAIL'];
  const password = process.env['NELLIS_PASSWORD'];
  const twoFactorCode = process.env['NELLIS_2FA_CODE'];
  const cookieFile = process.env['NELLIS_COOKIE_FILE'];

  if (!email || !password) {
    console.error('Skipping e2e login test: NELLIS_EMAIL / NELLIS_PASSWORD not set.');
    process.exit(0);
  }

  console.log(`[e2e] Attempting login for ${email}…`);

  const result = await login({ email, password, twoFactorCode, cookieFile });

  if (result.needsTwoFactor && !result.success) {
    console.warn('[e2e] 2FA required but NELLIS_2FA_CODE was not provided.');
    console.warn('[e2e] Re-run with NELLIS_2FA_CODE=<sms code> to complete login.');
    process.exit(0);
  }

  if (!result.success) {
    console.error(`[e2e] Login FAILED: ${result.message}`);
    process.exit(1);
  }

  console.log(`[e2e] Login SUCCEEDED: ${result.message}`);
}

runE2ELogin().catch((err: unknown) => {
  console.error('[e2e] Unexpected error:', err);
  process.exit(1);
});
