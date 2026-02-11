import type { TickLiquidity } from './api.ts';

export interface ProcessedRow {
	lowerTick: number;
	upperTick: number;
	liquidityAmount: number;
	tickRange: number;
}

export interface Stats {
	mean: number;
	median: number;
	stdDev: number;
	count: number;
}

/**
 * Parses raw API tick data into numeric rows with computed tick_range.
 * @param raw - Array of tick liquidity entries from the API
 * @returns Parsed rows with numeric fields
 */
export function parseRows(raw: TickLiquidity[]): ProcessedRow[] {
	return raw.map((r) => {
		const lowerTick = Number(r.lower_tick);
		const upperTick = Number(r.upper_tick);
		return {
			lowerTick,
			upperTick,
			liquidityAmount: Number(r.liquidity_amount),
			tickRange: upperTick - lowerTick,
		};
	});
}

/**
 * Returns the value at the given quantile (0-1) for a sorted numeric array.
 */
function quantile(sorted: number[], q: number): number {
	const pos = (sorted.length - 1) * q;
	const lo = Math.floor(pos);
	const hi = Math.ceil(pos);
	if (lo === hi) return sorted[lo];
	return sorted[lo] + (pos - lo) * (sorted[hi] - sorted[lo]);
}

/**
 * Filters rows below the 99th percentile for both liquidityAmount and tickRange,
 * matching the Python script's outlier removal.
 * @param rows - Parsed data rows
 * @returns Filtered subset
 */
export function filterOutliers(rows: ProcessedRow[]): ProcessedRow[] {
	if (rows.length === 0) return rows;

	const sortedLiq = rows.map((r) => r.liquidityAmount).sort((a, b) => a - b);
	const sortedRange = rows.map((r) => r.tickRange).sort((a, b) => a - b);

	const liqThreshold = quantile(sortedLiq, 0.99);
	const rangeThreshold = quantile(sortedRange, 0.99);

	return rows.filter((r) => r.liquidityAmount < liqThreshold && r.tickRange < rangeThreshold);
}

/**
 * Computes summary statistics for the liquidity_amount column (on full data, pre-filter).
 * @param rows - All parsed rows (not filtered)
 * @returns Mean, median, standard deviation, and count
 */
export function computeStats(rows: ProcessedRow[]): Stats {
	const n = rows.length;
	if (n === 0) return { mean: 0, median: 0, stdDev: 0, count: 0 };

	const vals = rows.map((r) => r.liquidityAmount);
	const sum = vals.reduce((a, b) => a + b, 0);
	const mean = sum / n;

	const sorted = [...vals].sort((a, b) => a - b);
	const median = n % 2 === 1 ? sorted[Math.floor(n / 2)] : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;

	const variance = vals.reduce((acc, v) => acc + (v - mean) ** 2, 0) / (n - 1);
	const stdDev = Math.sqrt(variance);

	return { mean, median, stdDev, count: n };
}
