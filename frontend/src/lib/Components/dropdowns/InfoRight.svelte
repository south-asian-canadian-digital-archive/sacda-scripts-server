<script lang="ts">
	import InputWithOption from '$lib/Components/inputs/WithOption.svelte';
	import Arrow from '$lib/Icons/Arrow.svelte';
	import { clickOutside } from '../../../utils/clickOutside';
	import { slide } from 'svelte/transition';
	import InfoRight from '../inputs/InfoRight.svelte';

	export let label: string;
	export let value = '';
	export let caption: string;
	export let placeholder = '';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	export let infoValue = '';
	export let defaultValue = '';
	export let options: string[] = [];

	export let dropdownOpen = false;
	export let inputFocused = false;
	$: dropdownClicked = false;

	$: {
		dropdownOpen = inputFocused || dropdownClicked;
	}
</script>

<div class="relative">
	<InfoRight
		bind:label
		bind:caption
		bind:value
		bind:placeholder
		bind:danger
		bind:dangerMessage
		bind:infoFocus={inputFocused}
		on:submit
	>
		<div
			class="flex flex-row justify-center items-center gap-1.5 cursor-pointer"
			on:click|stopPropagation={() => {
				dropdownOpen = !dropdownOpen;
				inputFocused = dropdownOpen;
			}}
			on:keydown
		>
			<span>{infoValue || defaultValue || options[0] || 'AM'}</span>
			<span
				class="cursor-pointer ease-in-out duration-200 transform select-none"
				class:-rotate-180={dropdownOpen}
				><Arrow />
			</span>
		</div>
	</InfoRight>
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
							infoValue = option;
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
		@apply overflow-y-auto right-0 w-4/6 absolute z-50 bg-white max-h-[200px] rounded-10 border border-[#EAF0ED] text-sm font-medium flex flex-col;
		box-shadow: 0px 12px 16px -4px rgba(16, 24, 40, 0.08), 0px 4px 6px -2px rgba(16, 24, 40, 0.03);
	}
</style>
