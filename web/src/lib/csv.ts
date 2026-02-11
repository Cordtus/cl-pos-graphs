import type { ProcessedRow } from './processing.ts';

/**
 * Triggers a CSV download in the browser via Blob API.
 * @param rows - Data rows to export
 * @param poolId - Pool ID for the filename
 * @param blockHeight - Optional block height for the filename
 */
export function downloadCsv(rows: ProcessedRow[], poolId: string, blockHeight?: string): void {
	const header = 'lower_tick,upper_tick,liquidity_amount,tick_range';
	const lines = rows.map(
		(r) => `${r.lowerTick},${r.upperTick},${r.liquidityAmount},${r.tickRange}`
	);
	const content = [header, ...lines].join('\n');

	const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
	const url = URL.createObjectURL(blob);

	const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
	const heightPart = blockHeight ? `_height_${blockHeight}` : '';
	const filename = `pool_${poolId}${heightPart}_${ts}.csv`;

	const a = document.createElement('a');
	a.href = url;
	a.download = filename;
	a.click();
	URL.revokeObjectURL(url);
}
