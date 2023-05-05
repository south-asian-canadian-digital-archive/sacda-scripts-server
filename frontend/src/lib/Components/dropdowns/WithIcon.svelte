<script lang="ts">
	import { slide } from 'svelte/transition';
	import Default from './Default.svelte';

	export let label;
	export let caption;
	export let options: {
		icon;
		text: string;
	}[] = [];
	export let selectedValues: string[] = [];
	export let placeholder = '';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	let dropdownOpen = false;
	let inputFocused = false;
</script>

<Default
	bind:label
	bind:caption
	bind:placeholder
	bind:danger
	bind:dangerMessage
	bind:dropdownOpen
	bind:inputFocused
	bind:selectedValues
>
	{#each options as option}
		<div
			class="flex flex-row items-center justify-start gap-3 px-4 py-3 cursor-pointer border-y hover:border-[#F2F4F7] border-white"
			on:keydown
			on:click={() => {
				dropdownOpen = false;
				inputFocused = false;
				selectedValues = [...selectedValues, option.text];
			}}
			transition:slide={{ duration: 100 }}
		>
			{#if option.icon}
				<div class="rounded-full object-cover w-10 h-10 mx-2">
					<svelte:component this={option.icon} />
				</div>
				<!-- {:else}
					<div class="w-10 h-10 rounded-full bg-[#21252914]" /> -->
			{/if}
			<div class="flex flex-col justify-evenly">
				<span class="text-[#34544C] text-sm">{option.text}</span>
			</div>
		</div>
	{/each}
</Default>
