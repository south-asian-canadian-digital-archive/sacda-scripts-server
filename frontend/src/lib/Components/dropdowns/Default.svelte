<script lang="ts">
	import InputWithOption from '../inputs/WithOption.svelte';
	import Arrow from '../../Icons/Arrow.svelte';
	import { clickOutside } from '../../../utils/clickOutside';
	import { slide } from 'svelte/transition';

	export let label: string;
	export let caption: string;
	export let placeholder = '';
	export let danger: boolean = false;
	export let dangerMessage: string = '';
	export let name: string = '';

	export let multiple = false;
	export let value = '';
	export let options: string[] = [];
	export let selectedValues: string[] = [];

	export let dropdownOpen = false;
	export let inputFocused = false;
	$: dropdownClicked = false;

	export let notReadOnly = false;

	export let selectedValuesBuffer: {
		icon: string;
		title: string;
		description: string;
		value: string;
	}[] = [];

	$: {
		dropdownOpen = inputFocused || dropdownClicked;
	}
</script>

<div
	class="relative"
	use:clickOutside
	on:click_outside={() => {
		dropdownOpen = false;
	}}
	on:click={() => {
		if (inputFocused) return;
		inputFocused = true;
	}}
	on:keydown
>
	<InputWithOption
		bind:label
		bind:caption
		bind:searchValue={value}
		bind:placeholder
		bind:danger
		bind:dangerMessage
		bind:selectedValues={selectedValuesBuffer}
		bind:focus={inputFocused}
		readonly={!notReadOnly}
		cursorPointer={!notReadOnly}
		on:submit
		bind:name
	>
		<slot name="icon">
			<div
				class="cursor-pointer ease-in-out duration-200 transform select-none"
				class:-rotate-180={dropdownOpen}
				on:click|stopPropagation={() => {
					dropdownOpen = !dropdownOpen;
					inputFocused = dropdownOpen;
				}}
				on:keydown
			>
				<Arrow />
			</div>
		</slot>
	</InputWithOption>
	{#if dropdownOpen}
		<div
			class="dropdown"
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
		>
			<slot>
				{#each options as option}
					<div
						class="flex flex-row items-center border-y hover:border-[#F2F4F7] border-white px-4 py-3 cursor-pointer text-[#34544C]"
						on:keydown
						on:click|stopPropagation={() => {
							dropdownOpen = false;
							inputFocused = false;
							if (selectedValues.includes(option)) return;
							if (multiple) {
								selectedValues = [...selectedValues, option];
								selectedValuesBuffer = [
									...selectedValuesBuffer,
									{
										icon: '',
										title: option,
										description: '',
										value: option
									}
								];
							} else {
								value = option;
							}
						}}
						transition:slide={{ duration: 100 }}
					>
						{option}
					</div>
				{/each}
			</slot>
		</div>
	{/if}
</div>

<style type="postcss">
	.dropdown {
		@apply overflow-y-auto absolute z-50 bg-white w-full max-h-[200px] rounded-[10px] border border-[#EAF0ED] text-sm font-medium flex flex-col;
		box-shadow: 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03);
	}
</style>
