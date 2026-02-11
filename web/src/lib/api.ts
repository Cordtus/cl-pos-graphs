import { ENDPOINTS } from './endpoints.ts';

const QUERY_PATH = '/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range';
const TIMEOUT_MS = 8000;

export interface TickLiquidity {
	liquidity_amount: string;
	lower_tick: string;
	upper_tick: string;
}

export interface ApiResponse {
	liquidity: TickLiquidity[];
}

export interface FetchResult {
	data: ApiResponse;
	endpoint: string;
}

/**
 * Fetches liquidity per tick range for a pool, trying endpoints in order.
 * @param poolId - Osmosis pool ID
 * @param blockHeight - Optional block height to query at
 * @returns The API response and which endpoint succeeded
 * @throws If all endpoints fail
 */
export async function fetchLiquidity(poolId: string, blockHeight?: string): Promise<FetchResult> {
	const errors: string[] = [];

	for (const endpoint of ENDPOINTS) {
		try {
			const url = new URL(QUERY_PATH, endpoint);
			url.searchParams.set('pool_id', poolId);

			const headers: Record<string, string> = { 'Content-Type': 'application/json' };
			if (blockHeight) {
				headers['x-cosmos-block-height'] = blockHeight;
			}

			const controller = new AbortController();
			const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

			const res = await fetch(url.toString(), { headers, signal: controller.signal });
			clearTimeout(timer);

			if (!res.ok) {
				errors.push(`${endpoint}: HTTP ${res.status}`);
				continue;
			}

			const data: ApiResponse = await res.json();

			if (!data.liquidity || !Array.isArray(data.liquidity)) {
				errors.push(`${endpoint}: missing liquidity array in response`);
				continue;
			}

			return { data, endpoint };
		} catch (err) {
			const msg = err instanceof Error ? err.message : String(err);
			errors.push(`${endpoint}: ${msg}`);
		}
	}

	throw new Error(`All endpoints failed:\n${errors.join('\n')}`);
}
