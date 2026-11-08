/**
 * placeBid.ts
 *
 * Search for an item on nellisauction.com and place a bid on the first
 * matching result.
 */

import { AxiosInstance } from 'axios';

export const BASE_URL = 'https://www.nellisauction.com';
export const SEARCH_URL = `${BASE_URL}/search`;
export const BID_URL = `${BASE_URL}/api/bids`;

export interface SearchResult {
  productId: number;
  title: string;
  currentBid: number;
  url: string;
}

export interface BidOptions {
  productId: number;
  bidAmount: number;
}

export interface BidResult {
  success: boolean;
  message: string;
  raw?: unknown;
}

/**
 * Extract product IDs and current bid amounts from the Nellis search-results
 * HTML page.  The page embeds JSON inside a `<script id="__NEXT_DATA__">` tag.
 */
export function parseSearchResults(html: string): SearchResult[] {
  const results: SearchResult[] = [];

  // Try to extract __NEXT_DATA__ JSON (Next.js SSR payload)
  const nextDataMatch = html.match(/<script id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/i);
  if (nextDataMatch) {
    try {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const nextData = JSON.parse(nextDataMatch[1]) as any;
      // Dig into the Next.js page props where search results live
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      const items = nextData?.props?.pageProps?.searchResults?.items as Array<{
        productId: number;
        name: string;
        currentBid?: number;
        slug?: string;
      }> | undefined;
      if (Array.isArray(items)) {
        for (const item of items) {
          results.push({
            productId: item.productId,
            title: item.name,
            currentBid: item.currentBid ?? 0,
            url: `${BASE_URL}/product/${item.slug ?? item.productId}`,
          });
        }
      }
    } catch {
      // fall through to regex fallback below
    }
  }

  // Fallback: scan for data-product-id attributes
  if (results.length === 0) {
    const productRegex = /data-product-id="(\d+)"/g;
    let m: RegExpExecArray | null;
    while ((m = productRegex.exec(html)) !== null) {
      const productId = parseInt(m[1], 10);
      if (!results.find((r) => r.productId === productId)) {
        results.push({ productId, title: '', currentBid: 0, url: `${BASE_URL}/product/${productId}` });
      }
    }
  }

  return results;
}

/**
 * Search nellisauction.com for `query` and return the parsed results.
 */
export async function searchItems(client: AxiosInstance, query: string): Promise<SearchResult[]> {
  const response = await client.get(SEARCH_URL, {
    params: { query },
  });
  return parseSearchResults(response.data as string);
}

/**
 * Place a bid on a product.
 */
export async function placeBid(client: AxiosInstance, options: BidOptions): Promise<BidResult> {
  const payload = { productId: options.productId, bid: options.bidAmount };

  try {
    const response = await client.post(BID_URL, payload, {
      headers: { 'Content-Type': 'application/json' },
    });

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const data = response.data as any;
    const success = response.status >= 200 && response.status < 300;

    return {
      success,
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      message: success ? `Bid of $${options.bidAmount} placed on product ${options.productId}.` : String(data?.message ?? data),
      raw: data,
    };
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    return { success: false, message: `Bid request failed: ${msg}` };
  }
}
