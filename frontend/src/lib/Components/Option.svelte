<script lang="ts">
	import Close from '$lib/Icons/updates/Close.svelte';
	import { createEventDispatcher } from 'svelte';

	export let option: {
		icon: string;
		title: string;
		description: string;
		value: string;
	};

	const dispatch = createEventDispatcher();
</script>

<div class="flex flex-row items-center bg-[#F2F7F5] rounded-10 p-1 -my-1 w-fit">
	{#if option.icon}
		<div class="rounded-full object-cover w-5 h-5">
			<img src={option.icon} alt="" />
		</div>
		<!-- {:else}
		<div class="w-5 h-5 rounded-full bg-[#21252914]" /> -->
	{/if}
	<span class="text-[#47675B] text-sm pl-1 whitespace-nowrap">{option.title}</span>
	<span
		class="pt-0.5 cursor-pointer"
		on:click={() => {
			dispatch('remove-option');
		}}
		on:keydown
	>
		<Close color="#47675B" size="16" />
	</span>
</div>
