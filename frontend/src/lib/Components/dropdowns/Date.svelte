<script lang="ts">
	import { clickOutside } from '../../../utils/clickOutside';
	import { fly, slide } from 'svelte/transition';
	import IconRightInteractive from '../inputs/IconRightInteractive.svelte';
	import DefaultDatepicker from '../datepickers/Default.svelte';
	import CalendarWithDate from '../../Icons/CalendarWithDate.svelte';
	import Close from '../../Icons/Close.svelte';

	export let label: string;
	export let selectedDate: Date | null = null;
	export let caption: string;
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	export let dropdownOpen = false;
	export let inputFocused = false;

	$: value = selectedDate ? selectedDate.toLocaleDateString('en-IN').split('/').join(' / ') : '';
	let placeholder = 'DD / MM / YYYY';

	$: dropdownClicked = false;

	$: {
		dropdownOpen = inputFocused || dropdownClicked;
	}

	const isSameDate = (date1: Date, date2: Date) => {
		return (
			date1.getFullYear() === date2.getFullYear() &&
			date1.getMonth() === date2.getMonth() &&
			date1.getDate() === date2.getDate()
		);
	};
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
				<CalendarWithDate />
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
			<DefaultDatepicker
				bind:selectedDate
				on:select={(e) => {
					if (!(e.detail.old && e.detail.new)) return;
					if (isSameDate(e.detail.old, e.detail.new)) {
						selectedDate = null;
					}
				}}
			/>
		</div>
	{/if}
</div>

<style type="postcss">
	.dropdown {
		@apply overflow-y-auto right-0 absolute z-50 bg-white rounded-2xl text-sm font-medium flex flex-col;
		box-shadow: 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03);
	}
</style>
