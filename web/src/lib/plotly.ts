import type { ProcessedRow } from './processing.ts';

/**
 * Builds a Plotly 3D scatter trace from processed data.
 * @param rows - Filtered data rows for plotting
 * @param dotSize - Marker size (1-100)
 * @returns Plotly trace object
 */
export function buildTrace(rows: ProcessedRow[], dotSize: number): Plotly.Data {
	return {
		type: 'scatter3d',
		mode: 'markers',
		x: rows.map((r) => r.lowerTick),
		y: rows.map((r) => r.upperTick),
		z: rows.map((r) => r.liquidityAmount),
		marker: {
			size: Math.max(1, Math.min(dotSize / 10, 10)),
			color: rows.map((r) => r.liquidityAmount),
			colorscale: 'Viridis',
			colorbar: { title: 'Liquidity' },
			opacity: 0.8,
		},
		hovertemplate:
			'Lower Tick: %{x}<br>Upper Tick: %{y}<br>Liquidity: %{z:,.0f}<extra></extra>',
	};
}

/**
 * Builds a Plotly layout for the 3D scatter chart.
 * @param blockHeight - Optional block height for the title
 * @returns Plotly layout object
 */
export function buildLayout(blockHeight?: string): Partial<Plotly.Layout> {
	const title = blockHeight
		? `Liquidity Per Tick Range - Height ${blockHeight}`
		: 'Liquidity Per Tick Range';

	const axisStyle = {
		gridcolor: '#2a2a3a',
		zerolinecolor: '#2a2a3a',
		showbackground: true,
		backgroundcolor: '#0e0e16',
	};

	return {
		title: { text: title },
		scene: {
			aspectmode: 'cube' as const,
			xaxis: { title: { text: 'Lower Tick', standoff: 10 }, ...axisStyle },
			yaxis: { title: { text: 'Upper Tick', standoff: 10 }, ...axisStyle },
			zaxis: { title: { text: 'Liquidity Amount', standoff: 10 }, ...axisStyle },
			camera: {
				eye: { x: 1.5, y: 1.5, z: 1.2 },
				center: { x: 0, y: 0, z: -0.1 },
			},
		},
		margin: { l: 0, r: 0, t: 40, b: 0 },
		paper_bgcolor: '#0a0a0f',
		font: { color: '#c8c8d0' },
	};
}
