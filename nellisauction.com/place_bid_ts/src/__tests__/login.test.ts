import { responseRequiresTwoFactor, responseIndicatesSuccess, createClient, saveCookies } from '../login';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

describe('responseRequiresTwoFactor', () => {
  it('returns true when response contains "verification_code"', () => {
    expect(responseRequiresTwoFactor('<form><input name="verification_code"/></form>')).toBe(true);
  });

  it('returns true when response contains "Enter the code"', () => {
    expect(responseRequiresTwoFactor('Please Enter the code sent to your phone')).toBe(true);
  });

  it('returns true when response contains "twoFactor"', () => {
    expect(responseRequiresTwoFactor(JSON.stringify({ twoFactor: true }))).toBe(true);
  });

  it('returns false for normal login page', () => {
    expect(responseRequiresTwoFactor('<form><input name="email"/><input name="password"/></form>')).toBe(false);
  });
});

describe('responseIndicatesSuccess', () => {
  it('returns true when response contains "dashboard"', () => {
    expect(responseIndicatesSuccess('<a href="/dashboard">Go to dashboard</a>')).toBe(true);
  });

  it('returns true when response contains "Log Out"', () => {
    expect(responseIndicatesSuccess('<a>Log Out</a>')).toBe(true);
  });

  it('returns false for unauthenticated page', () => {
    expect(responseIndicatesSuccess('<form id="login-form"></form>')).toBe(false);
  });
});

describe('createClient', () => {
  it('creates an axios instance', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nellis-test-'));
    const cookieFile = path.join(tmpDir, 'cookies.json');
    const client = createClient(cookieFile);
    expect(client).toBeDefined();
    expect(typeof client.get).toBe('function');
    expect(typeof client.post).toBe('function');
  });

  it('does not throw when cookie file does not exist', () => {
    expect(() => createClient('/tmp/nonexistent_cookie_file.json')).not.toThrow();
  });

  it('does not throw when cookie file is corrupt', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nellis-test-'));
    const cookieFile = path.join(tmpDir, 'bad_cookies.json');
    fs.writeFileSync(cookieFile, 'not-valid-json');
    expect(() => createClient(cookieFile)).not.toThrow();
  });
});

describe('saveCookies', () => {
  it('writes a JSON file', () => {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'nellis-test-'));
    const cookieFile = path.join(tmpDir, 'cookies.json');
    const client = createClient(cookieFile);
    saveCookies(client, cookieFile);
    expect(fs.existsSync(cookieFile)).toBe(true);
    const contents = fs.readFileSync(cookieFile, 'utf-8');
    expect(() => JSON.parse(contents)).not.toThrow();
  });
});
