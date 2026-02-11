<script lang="ts">
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>Osmosis CL Pool Visualizer</title>
	<meta name="description" content="3D visualization of Osmosis concentrated liquidity pool data" />
</svelte:head>

{@render children()}
