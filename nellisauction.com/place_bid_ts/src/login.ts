/**
 * login.ts
 *
 * Handles login to nellisauction.com with two-factor authentication.
 *
 * Flow:
 * 1. POST credentials to /login.
 * 2. If the response indicates a 2FA code is needed, submit the code
 *    that was provided via the NELLIS_2FA_CODE environment variable
 *    (or the `twoFactorCode` parameter).
 * 3. Persist the session cookies to a file so subsequent runs can
 *    reuse the session without logging in again.
 *
 * Two-factor code delivery in GitHub Actions:
 *   The workflow can be triggered with `workflow_dispatch` and accept
 *   a `two_factor_code` input.  The caller passes the code as the
 *   NELLIS_2FA_CODE environment variable to this script.
 */

import axios, { AxiosInstance } from 'axios';
import { wrapper } from 'axios-cookiejar-support';
import { CookieJar } from 'tough-cookie';
import * as fs from 'fs';
import * as path from 'path';

export const BASE_URL = 'https://www.nellisauction.com';
export const LOGIN_URL = `${BASE_URL}/login`;
export const TWO_FA_URL = `${BASE_URL}/api/verify-code`; // hypothetical 2FA endpoint

export const DEFAULT_COOKIE_FILE = path.join(process.cwd(), 'cookies.json');

export const DEFAULT_HEADERS = {
  'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  Accept:
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
};

export interface LoginOptions {
  email: string;
  password: string;
  /** 6-digit 2FA code sent to the registered phone number. */
  twoFactorCode?: string;
  /** Path to the cookie file used for session persistence. */
  cookieFile?: string;
}

export interface LoginResult {
  success: boolean;
  needsTwoFactor: boolean;
  message: string;
  /** The axios client that carries the authenticated session cookies. */
  client: AxiosInstance;
}

/**
 * Create an axios client backed by a persistent CookieJar.
 * If a cookie file already exists its contents are loaded into the jar.
 */
export function createClient(cookieFile: string = DEFAULT_COOKIE_FILE): AxiosInstance {
  const jar = new CookieJar();

  if (fs.existsSync(cookieFile)) {
    try {
      const raw = fs.readFileSync(cookieFile, 'utf-8');
      const loaded = CookieJar.fromJSON(raw);
      // Copy all cookies into our jar
      for (const cookie of loaded.toJSON().cookies ?? []) {
        jar.setCookieSync(
          `${cookie.key}=${cookie.value}; Domain=${cookie.domain}; Path=${cookie.path ?? '/'}`,
          BASE_URL
        );
      }
    } catch {
      // If the cookie file is corrupt just start fresh
    }
  }

  const instance = axios.create({ headers: DEFAULT_HEADERS, withCredentials: true });
  // axios-cookiejar-support augments AxiosRequestConfig with 'jar' but the
  // module declaration doesn't extend AxiosDefaults, so we cast here.
  (instance.defaults as Record<string, unknown>)['jar'] = jar;
  // wrapper() expects AxiosStatic | AxiosInstance; cast to satisfy the type.
  const client = wrapper(instance as Parameters<typeof wrapper>[0]);
  return client as AxiosInstance;
}

/**
 * Save the cookie jar of an axios client to disk for reuse in later runs.
 */
export function saveCookies(client: AxiosInstance, cookieFile: string = DEFAULT_COOKIE_FILE): void {
  // axios-cookiejar-support exposes the jar on the instance defaults
  const jar: CookieJar | undefined = (client.defaults as { jar?: CookieJar }).jar;
  if (!jar) return;
  fs.writeFileSync(cookieFile, JSON.stringify(jar.toJSON()), 'utf-8');
}

/**
 * Determine whether the response HTML / JSON indicates a 2FA challenge.
 */
export function responseRequiresTwoFactor(responseData: string | object): boolean {
  const text = typeof responseData === 'string' ? responseData : JSON.stringify(responseData);
  // The site may redirect to a /verify or show a form with 'verification_code'
  return (
    text.includes('verification_code') ||
    text.includes('verify-code') ||
    text.includes('two-factor') ||
    text.includes('twoFactor') ||
    text.includes('Enter the code') ||
    text.includes('enter the code')
  );
}

/**
 * Determine whether the response indicates a successful login
 * (i.e. we are now on a page that is only accessible when authenticated).
 */
export function responseIndicatesSuccess(responseData: string | object): boolean {
  const text = typeof responseData === 'string' ? responseData : JSON.stringify(responseData);
  // After login Nellis typically redirects to the dashboard or shows a
  // user-specific element.  We look for common authenticated-page signals.
  return (
    text.includes('dashboard') ||
    text.includes('My Account') ||
    text.includes('my-account') ||
    text.includes('Log Out') ||
    text.includes('logout')
  );
}

/**
 * Log in to nellisauction.com.
 *
 * @returns LoginResult describing the outcome and the authenticated client.
 */
export async function login(options: LoginOptions): Promise<LoginResult> {
  const cookieFile = options.cookieFile ?? DEFAULT_COOKIE_FILE;
  const client = createClient(cookieFile);

  // ── Step 1: POST credentials ──────────────────────────────────────────────
  const formData = new URLSearchParams();
  formData.set('__rvfInternalFormId', 'login');
  formData.set('email', options.email);
  formData.set('password', options.password);

  let loginResponse;
  try {
    loginResponse = await client.post(LOGIN_URL, formData.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      maxRedirects: 5,
    });
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    return { success: false, needsTwoFactor: false, message: `Login request failed: ${msg}`, client };
  }

  const loginData: string | object = loginResponse.data as string | object;

  // ── Step 2: Check whether 2FA is required ─────────────────────────────────
  if (responseRequiresTwoFactor(loginData)) {
    if (!options.twoFactorCode) {
      return {
        success: false,
        needsTwoFactor: true,
        message:
          'Two-factor authentication required. ' +
          'Set the NELLIS_2FA_CODE environment variable or pass twoFactorCode.',
        client,
      };
    }

    // Submit the 2FA code
    const tfaData = new URLSearchParams();
    tfaData.set('verification_code', options.twoFactorCode);

    let tfaResponse;
    try {
      tfaResponse = await client.post(TWO_FA_URL, tfaData.toString(), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        maxRedirects: 5,
      });
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      return {
        success: false,
        needsTwoFactor: true,
        message: `2FA submission failed: ${msg}`,
        client,
      };
    }

    if (!responseIndicatesSuccess(tfaResponse.data as string | object)) {
      return {
        success: false,
        needsTwoFactor: true,
        message: 'Login failed after 2FA submission. Check the code and try again.',
        client,
      };
    }

    saveCookies(client, cookieFile);
    return { success: true, needsTwoFactor: true, message: 'Logged in successfully (2FA).' , client };
  }

  // ── Step 3: Check for direct success ─────────────────────────────────────
  if (responseIndicatesSuccess(loginData)) {
    saveCookies(client, cookieFile);
    return { success: true, needsTwoFactor: false, message: 'Logged in successfully.', client };
  }

  // Neither success nor 2FA – credentials probably wrong
  return {
    success: false,
    needsTwoFactor: false,
    message: 'Login failed. Check your credentials.',
    client,
  };
}
