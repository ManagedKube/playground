import axios from 'axios';
import { parseSearchResults, searchItems, placeBid } from '../placeBid';

describe('parseSearchResults', () => {
  it('returns empty array for empty HTML', () => {
    expect(parseSearchResults('')).toEqual([]);
  });

  it('parses items from __NEXT_DATA__ JSON', () => {
    const nextData = {
      props: {
        pageProps: {
          searchResults: {
            items: [
              { productId: 12345, name: 'Test Item', currentBid: 10, slug: 'test-item' },
              { productId: 67890, name: 'Another Item', currentBid: 25, slug: 'another-item' },
            ],
          },
        },
      },
    };
    const html = `<html><head><script id="__NEXT_DATA__" type="application/json">${JSON.stringify(nextData)}</script></head></html>`;
    const results = parseSearchResults(html);
    expect(results).toHaveLength(2);
    expect(results[0]).toMatchObject({ productId: 12345, title: 'Test Item', currentBid: 10 });
    expect(results[1]).toMatchObject({ productId: 67890, title: 'Another Item', currentBid: 25 });
  });

  it('falls back to data-product-id attributes when __NEXT_DATA__ is absent', () => {
    const html = `
      <div data-product-id="111"></div>
      <div data-product-id="222"></div>
    `;
    const results = parseSearchResults(html);
    expect(results).toHaveLength(2);
    expect(results.map((r) => r.productId)).toEqual([111, 222]);
  });

  it('deduplicates product IDs from data-product-id attributes', () => {
    const html = `
      <div data-product-id="111"></div>
      <div data-product-id="111"></div>
    `;
    const results = parseSearchResults(html);
    expect(results).toHaveLength(1);
  });

  it('uses productId as slug fallback when slug is absent', () => {
    const nextData = {
      props: {
        pageProps: {
          searchResults: {
            items: [{ productId: 99999, name: 'No Slug', currentBid: 5 }],
          },
        },
      },
    };
    const html = `<script id="__NEXT_DATA__" type="application/json">${JSON.stringify(nextData)}</script>`;
    const results = parseSearchResults(html);
    expect(results[0]!.url).toContain('99999');
  });
});

describe('searchItems', () => {
  it('calls GET /search with the query param and returns parsed results', async () => {
    const fakeHtml = `<div data-product-id="55555"></div>`;
    const mockGet = jest.fn().mockResolvedValue({ data: fakeHtml });
    const mockClient = { get: mockGet } as unknown as ReturnType<typeof axios.create>;

    const results = await searchItems(mockClient, 'vacuum cleaner');
    expect(mockGet).toHaveBeenCalledWith(
      expect.stringContaining('/search'),
      expect.objectContaining({ params: { query: 'vacuum cleaner' } })
    );
    expect(results[0]!.productId).toBe(55555);
  });
});

describe('placeBid', () => {
  it('returns success when the API responds with 2xx', async () => {
    const mockPost = jest.fn().mockResolvedValue({ status: 200, data: { ok: true } });
    const mockClient = { post: mockPost } as unknown as ReturnType<typeof axios.create>;

    const result = await placeBid(mockClient, { productId: 12345, bidAmount: 15 });
    expect(result.success).toBe(true);
    expect(result.message).toContain('12345');
    expect(result.message).toContain('15');
  });

  it('returns failure when the API call throws', async () => {
    const mockPost = jest.fn().mockRejectedValue(new Error('Network error'));
    const mockClient = { post: mockPost } as unknown as ReturnType<typeof axios.create>;

    const result = await placeBid(mockClient, { productId: 12345, bidAmount: 15 });
    expect(result.success).toBe(false);
    expect(result.message).toContain('Network error');
  });
});
