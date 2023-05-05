<script lang="ts">
	import { clickOutside } from '$utils/clickOutside';
	import { fly, slide } from 'svelte/transition';
	import IconRightInteractive from '../inputs/IconRightInteractive.svelte';
	import RangeDatepicker from '../datepickers/Range.svelte';
	import Close from '$lib/Icons/updates/Close.svelte';
	import Calendar from '$lib/Icons/updates/Calendar.svelte';

	export let label;
	export let caption;
	export let startDate: Date = null;
	export let endDate: Date = null;
	export let selectedRange: Date[] = [];
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	export let dropdownOpen = false;
	export let inputFocused = false;

	$: value = startDate
		? `${startDate.toLocaleDateString().split('/').join(' / ')} - ${
				endDate ? endDate.toLocaleDateString('en-IN').split('/').join(' / ') : 'DD / MM / YYYY'
		  }`
		: '';

	let placeholder = 'DD / MM / YYYY - DD / MM / YYYY';
	$: dropdownClicked = false;

	$: {
		dropdownOpen = inputFocused || dropdownClicked;
	}
</script>

<div class="relative w-full">
	<IconRightInteractive
		bind:label
		bind:caption
		bind:value
		bind:placeholder
		bind:danger
		bind:dangerMessage
		bind:inputFocused
		on:submit
	>
		<div
			class="flex flex-row justify-center items-center cursor-pointer select-none"
			on:click|stopPropagation={() => {
				dropdownOpen = !dropdownOpen;
				inputFocused = dropdownOpen;
			}}
			on:keydown
		>
			{#if !dropdownOpen}
				<Calendar />
			{:else}
				<Close size="24" color="#0F9D58" />
			{/if}
		</div>
	</IconRightInteractive>
	{#if dropdownOpen}
		<div
			class="dropdown w-full"
			class:-mt-4={!caption}
			class:mt-1={caption}
			on:keydown
			on:click={() => {
				dropdownClicked = true;
			}}
			use:clickOutside
			on:click_outside={() => {
				dropdownClicked = false;
			}}
			in:slide={{ duration: 200 }}
			out:slide={{ duration: 200 }}
		>
			<RangeDatepicker bind:startDate bind:endDate bind:selectedRange />
		</div>
	{/if}
</div>

<style type="postcss">
	.dropdown {
		@apply overflow-y-auto right-0 absolute z-50 bg-white rounded-2xl text-sm font-medium flex flex-col;
		box-shadow: 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03);
	}
</style>
