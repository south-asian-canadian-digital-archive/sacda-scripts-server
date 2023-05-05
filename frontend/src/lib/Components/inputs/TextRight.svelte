<script lang="ts">
	import InfoRight from './InfoRight.svelte';

	export let value;
	export let label = '';
	export let caption = '';
	export let text = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';
</script>

{#key text}
	<InfoRight
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
	</InfoRight>
{/key}
