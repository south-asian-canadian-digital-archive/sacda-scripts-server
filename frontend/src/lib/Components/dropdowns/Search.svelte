<script lang="ts">
	import { slide } from 'svelte/transition';
	import Default from './Default.svelte';
	import Close from '$lib/Icons/Close.svelte';
	import Loader from '$lib/Icons/Loader.svelte';
	import Input from '../inputs/Main.svelte';
	import ButtonPrimary from '../buttons/primary/Default.svelte';
	import ButtonSecondary from '../buttons/secondary/Default.svelte';
	import { createEventDispatcher } from 'svelte';
	import Warning from '$lib/Icons/warning.svelte';

	export let label: string;
	export let caption: string;
	export let value: string;
	export let options: string[] = [];
	export let placeholder = '';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	let selectedValuesBuffer = [];

	let dropdownOpen = false;
	let inputFocused = false;

	let loading = false;
	let addMode = false;
	let dispatch = createEventDispatcher();

	$: {
		if (!inputFocused) {
			addMode = false;
		}
	}

	// ----------- search ------------

	$: filteredOptions = options.filter((option) => {
		return option.toLowerCase().includes(value.toLowerCase());
	});

	const searchValue = (option) => {
		value = option;
	};

	// ----------- for add mode ------------

	let addModeInputCaption = 'Caption goes here';
	let addModeInputValue = '';

	// -------------------------------------
</script>

<Default
	bind:label
	bind:caption
	bind:placeholder
	bind:danger
	bind:dangerMessage
	bind:dropdownOpen
	bind:inputFocused
	bind:value
	bind:selectedValuesBuffer
	notReadOnly
	on:submit={() => {
		// to prevent options from being selected when the user presses enter
		selectedValuesBuffer = [];
	}}
>
	<div
		slot="icon"
		on:click={() => {
			value = '';
		}}
		on:keydown
	>
		{#if value}
			<Close />
		{/if}
	</div>

	{#if !loading}
		{#if addMode}
			<div class="p-4 -mt-7 flex flex-col items-center gap-3" transition:slide={{ duration: 100 }}>
				<Input
					autofocus
					label=""
					bind:caption={addModeInputCaption}
					bind:value={addModeInputValue}
				/>
				<div
					class="border-t border-[#F2F4F7] w-full flex flex-row items-center justify-between pt-3"
				>
					<div class="flex flex-row gap-2">
						<ButtonPrimary
							size="xs"
							label="Create"
							on:click={() => {
								dispatch('create', addModeInputValue);
								loading = true;
								setTimeout(() => {
									loading = false;
									addMode = false;
								}, 150);
							}}
						/>
						<ButtonSecondary
							size="xs"
							label="Cancel"
							on:click={() => {
								loading = true;
								setTimeout(() => {
									loading = false;
									addMode = false;
								}, 150);
							}}
						/>
					</div>
					<span class="text-xs text-[#98B3AB]">
						{addModeInputValue.length}/50
					</span>
				</div>
			</div>
		{:else}
			{#each filteredOptions as option}
				<div
					class="flex flex-row items-center border-y hover:border-[#F2F4F7] border-white px-4 py-3 cursor-pointer text-[#34544C]"
					on:keydown
					on:click|stopPropagation={() => {
						dropdownOpen = false;
						inputFocused = false;

						value = option;
					}}
					transition:slide={{ duration: 100 }}
				>
					{option}
				</div>
			{:else}
				<div>
					<div
						class="flex flex-col items-center justify-center gap-3 pb-7 pt-6 border-b border-[#F2F4F7]"
					>
						<Warning />
						<span class="text-[#47675B] text-sm font-semibold"> No results found </span>
					</div>

					<div class="flex flex-col justify-center gap-2 py-3">
						<span class="text-[#2125298F] text-xs font-normal text-center">Try searching for</span>
						<div class="flex flex-row gap-2 justify-center items-center">
							{#each [options[Math.floor(Math.random() * options.length)], options[Math.floor(Math.random() * options.length)], options[Math.floor(Math.random() * options.length)]] as i}
								<div
									class="py-1 px-3 text-[#34544C] flex text-xs border border-dashed border-[#D0DDD7] rounded-[32px] cursor-pointer"
									on:click={() => {
										console.log('click');
									}}
									on:keydown
								>
									{i}
								</div>
							{/each}
						</div>
					</div>
				</div>
			{/each}
			{#if filteredOptions.length}
				<div
					class="border-t border-[#EAF0ED] text-[#0F9D58] font-semibold text-sm px-4 py-3 cursor-pointer flex flex-row items-center gap-3"
					on:click={() => {
						loading = true;
						setTimeout(() => {
							loading = false;
							addMode = true;
						}, 150);
					}}
					on:keydown
					transition:slide={{ duration: 100 }}
				>
					<span class=" rotate-45"><Close color="#0F9D58" /></span> Add new
				</div>{/if}
		{/if}
	{:else}
		<div class="flex items-center justify-center py-5" transition:slide={{ duration: 100 }}>
			<Loader size="38" />
		</div>
	{/if}
</Default>
