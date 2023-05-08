<script lang="ts">
	import InfoLeft from './InfoLeft.svelte';

	export let value: string;
	export let label = '';
	export let caption = '';
	export let text = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';
</script>

{#key text}
	<InfoLeft
		bind:value
		bind:label
		bind:caption
		bind:danger
		bind:dangerMessage
		bind:placeholder
		on:change
	>
		<span>
			{#if text}{text}{:else}&nbsp;{/if}
		</span>
	</InfoLeft>
{/key}
