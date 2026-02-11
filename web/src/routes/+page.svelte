<script lang="ts">
	import { fetchLiquidity } from '$lib/api.ts';
	import { parseRows, filterOutliers, computeStats, type ProcessedRow, type Stats } from '$lib/processing.ts';
	import { downloadCsv } from '$lib/csv.ts';
	import { buildTrace, buildLayout } from '$lib/plotly.ts';
	import { browser } from '$app/environment';

	let poolId = $state('1388');
	let blockHeight = $state('');
	let dotSize = $state(30);
	let loading = $state(false);
	let error = $state('');
	let usedEndpoint = $state('');

	let allRows = $state<ProcessedRow[]>([]);
	let filtered = $state<ProcessedRow[]>([]);
	let stats = $state<Stats | null>(null);

	let chartDiv: HTMLDivElement | undefined = $state();
	let Plotly: typeof import('plotly.js-dist-min') | null = $state(null);

	async function loadPlotly() {
		if (Plotly || !browser) return;
		Plotly = await import('plotly.js-dist-min');
	}

	async function handleFetch() {
		if (!poolId.trim()) return;
		loading = true;
		error = '';
		usedEndpoint = '';

		try {
			const height = blockHeight.trim() || undefined;
			const { data, endpoint } = await fetchLiquidity(poolId.trim(), height);
			usedEndpoint = endpoint;

			allRows = parseRows(data.liquidity);
			filtered = filterOutliers(allRows);
			stats = computeStats(allRows);

			await loadPlotly();
			renderChart();
		} catch (err) {
			error = err instanceof Error ? err.message : String(err);
			allRows = [];
			filtered = [];
			stats = null;
		} finally {
			loading = false;
		}
	}

	function renderChart() {
		if (!Plotly || !chartDiv || filtered.length === 0) return;
		const trace = buildTrace(filtered, dotSize);
		const layout = buildLayout(blockHeight.trim() || undefined);
		Plotly.newPlot(chartDiv, [trace], layout, { responsive: true });
		invertDrag();
	}

	function invertDrag() {
		if (!chartDiv) return;
		const canvas = chartDiv.querySelector('.gl-container canvas');
		if (!canvas) return;

		let lastX = 0;
		let lastY = 0;
		let dragging = false;

		canvas.addEventListener('pointerdown', ((e: PointerEvent) => {
			lastX = e.clientX;
			lastY = e.clientY;
			dragging = true;
		}) as EventListener);

		window.addEventListener('pointermove', ((e: PointerEvent) => {
			if (!dragging || !chartDiv || !Plotly) return;
			const scene = (chartDiv as any)._fullLayout?.scene?._scene;
			if (!scene?.camera) return;

			const dx = e.clientX - lastX;
			const dy = e.clientY - lastY;
			lastX = e.clientX;
			lastY = e.clientY;

			const cam = scene.camera;
			if (typeof cam.rotate === 'function') {
				e.preventDefault();
				e.stopPropagation();
				cam.rotate(-dx, -dy);
			}
		}) as EventListener, { capture: true });

		window.addEventListener('pointerup', () => { dragging = false; });
	}

	function handleExportCsv() {
		if (allRows.length === 0) return;
		downloadCsv(allRows, poolId.trim(), blockHeight.trim() || undefined);
	}

	function handleDotSizeChange() {
		if (filtered.length > 0 && Plotly && chartDiv) {
			renderChart();
		}
	}

	function formatNumber(n: number): string {
		if (Math.abs(n) >= 1e9) return (n / 1e9).toFixed(2) + 'B';
		if (Math.abs(n) >= 1e6) return (n / 1e6).toFixed(2) + 'M';
		if (Math.abs(n) >= 1e3) return (n / 1e3).toFixed(2) + 'K';
		return n.toFixed(2);
	}
</script>

<main>
	<header>
		<h1>Osmosis CL Pool Visualizer</h1>
		<p class="subtitle">Concentrated liquidity 3D scatter plots</p>
	</header>

	<section class="controls">
		<div class="field">
			<label for="pool-id">Pool ID</label>
			<input
				id="pool-id"
				type="text"
				bind:value={poolId}
				placeholder="e.g. 1388"
				onkeydown={(e) => e.key === 'Enter' && handleFetch()}
			/>
		</div>

		<div class="field">
			<label for="block-height">Block Height <span class="optional">(optional)</span></label>
			<input
				id="block-height"
				type="text"
				bind:value={blockHeight}
				placeholder="latest"
				onkeydown={(e) => e.key === 'Enter' && handleFetch()}
			/>
		</div>

		<div class="field">
			<label for="dot-size">Dot Size: {dotSize}</label>
			<input
				id="dot-size"
				type="range"
				min="1"
				max="100"
				bind:value={dotSize}
				onchange={handleDotSizeChange}
			/>
		</div>

		<div class="actions">
			<button class="btn-primary" onclick={handleFetch} disabled={loading || !poolId.trim()}>
				{loading ? 'Fetching...' : 'Fetch Data'}
			</button>
			<button class="btn-secondary" onclick={handleExportCsv} disabled={allRows.length === 0}>
				Export CSV
			</button>
		</div>
	</section>

	{#if error}
		<div class="error-banner">{error}</div>
	{/if}

	{#if usedEndpoint}
		<p class="endpoint-info">Endpoint: <code>{usedEndpoint}</code></p>
	{/if}

	{#if stats}
		<section class="stats-grid">
			<div class="stat-card">
				<span class="stat-label">Mean</span>
				<span class="stat-value">{formatNumber(stats.mean)}</span>
			</div>
			<div class="stat-card">
				<span class="stat-label">Median</span>
				<span class="stat-value">{formatNumber(stats.median)}</span>
			</div>
			<div class="stat-card">
				<span class="stat-label">Std Dev</span>
				<span class="stat-value">{formatNumber(stats.stdDev)}</span>
			</div>
			<div class="stat-card">
				<span class="stat-label">Count</span>
				<span class="stat-value">{stats.count.toLocaleString()}</span>
			</div>
			<div class="stat-card">
				<span class="stat-label">Plotted</span>
				<span class="stat-value">{filtered.length.toLocaleString()}</span>
			</div>
		</section>
	{/if}

	<section class="chart-container">
		<div bind:this={chartDiv} class="chart"></div>
	</section>
</main>

<style>
	main {
		max-width: 1200px;
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}

	header {
		margin-bottom: 2rem;
	}

	h1 {
		font-size: 1.5rem;
		font-weight: 600;
		letter-spacing: -0.02em;
	}

	.subtitle {
		color: var(--text-secondary);
		font-size: 0.875rem;
		margin-top: 0.25rem;
	}

	.controls {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		align-items: flex-end;
		padding: 1.25rem;
		background: var(--bg-secondary);
		border: 1px solid var(--border);
		border-radius: 8px;
		margin-bottom: 1rem;
	}

	.field {
		display: flex;
		flex-direction: column;
		gap: 0.375rem;
	}

	.field label {
		font-size: 0.75rem;
		font-weight: 500;
		color: var(--text-secondary);
		text-transform: uppercase;
		letter-spacing: 0.05em;
	}

	.optional {
		text-transform: none;
		letter-spacing: normal;
		opacity: 0.6;
	}

	.field input[type="text"] {
		width: 160px;
	}

	.field input[type="range"] {
		width: 120px;
		accent-color: var(--accent);
	}

	.actions {
		display: flex;
		gap: 0.5rem;
		margin-left: auto;
	}

	.btn-primary {
		background: var(--accent);
		color: #fff;
		font-weight: 500;
	}

	.btn-primary:hover:not(:disabled) {
		background: var(--accent-hover);
	}

	.btn-secondary {
		background: var(--bg-tertiary);
		color: var(--text-primary);
		border: 1px solid var(--border);
	}

	.btn-secondary:hover:not(:disabled) {
		background: var(--border);
	}

	.error-banner {
		background: rgba(224, 85, 85, 0.1);
		border: 1px solid var(--danger);
		border-radius: 6px;
		color: var(--danger);
		padding: 0.75rem 1rem;
		font-size: 0.8125rem;
		font-family: var(--font-mono);
		white-space: pre-wrap;
		margin-bottom: 1rem;
	}

	.endpoint-info {
		font-size: 0.75rem;
		color: var(--text-secondary);
		margin-bottom: 1rem;
	}

	.endpoint-info code {
		font-family: var(--font-mono);
		color: var(--success);
	}

	.stats-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
		gap: 0.75rem;
		margin-bottom: 1rem;
	}

	.stat-card {
		background: var(--bg-secondary);
		border: 1px solid var(--border);
		border-radius: 8px;
		padding: 0.875rem 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.stat-label {
		font-size: 0.6875rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--text-secondary);
	}

	.stat-value {
		font-family: var(--font-mono);
		font-size: 1.125rem;
		font-weight: 600;
	}

	.chart-container {
		background: var(--bg-secondary);
		border: 1px solid var(--border);
		border-radius: 8px;
		overflow: hidden;
	}

	.chart {
		width: 100%;
		height: 600px;
	}

	@media (max-width: 640px) {
		.controls {
			flex-direction: column;
			align-items: stretch;
		}

		.field input[type="text"] {
			width: 100%;
		}

		.actions {
			margin-left: 0;
		}

		.chart {
			height: 400px;
		}
	}
</style>
