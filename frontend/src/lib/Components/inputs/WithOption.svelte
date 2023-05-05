<script lang="ts">
	import Arrow from '$lib/Icons/updates/Arrow.svelte';
	import { createEventDispatcher } from 'svelte';
	import Option from '../Option.svelte';
	import { clickOutside } from '$utils/clickOutside';

	export let selectedValues: {
		icon: string;
		title: string;
		description: string;
		value: string;
	}[] = [];
	// export let options: {
	// 	icon: string;
	// 	title: string;
	// 	description: string;
	// 	value: string;
	// }[] = [];
	export let label = '';
	export let caption = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';
	export let focus = false;
	export let readonly = false;
	export let cursorPointer = false;

	export let searchValue = '';

	const dispatch = createEventDispatcher();

	function handleSubmit() {
		if (searchValue === '') {
			return;
		}

		// example
		// selectedValues = [
		// 	...selectedValues,
		// 	{
		// 		icon: null,
		// 		title: searchValue,
		// 		description: '',
		// 		value: searchValue
		// 	}
		// ];

		// searchValue = '';

		dispatch('submit', selectedValues);
	}
</script>

<div class="flex flex-col items-start gap-2 w-full">
	<label class="text-[#47675B] font-medium text-sm" for="">
		{#if label}{label}{:else}&nbsp;{/if}
	</label>
	<div
		class="relative w-full flex items-center pr-11 min-h-[54px] border border-[#D0DDD7] rounded-14 p-4 ease-out duration-100"
		use:clickOutside
		on:keydown
		on:click={() => {
			focus = true;
			dispatch('click');
		}}
		on:click_outside={() => {
			focus = false;
		}}
		class:input-selected={focus}
		class:input-danger={danger}
		class:input-danger-focus={danger && focus}
	>
		<div class="overflow-y-auto flex items-center gap-2 w-full">
			{#each selectedValues as value, key}
				<Option
					on:remove-option={() => {
						selectedValues = selectedValues.filter((_, index) => index !== key);
						dispatch('remove-option', selectedValues);
					}}
					option={value}
				/>
			{/each}

			<input
				type="text"
				class="placeholder:text-[#98B3AB] text-[#47675B] outline-none w-full min-w-[100px]"
				bind:value={searchValue}
				on:keydown={(event) => {
					if (event.key === 'Enter') {
						handleSubmit();
					} else if (event.key === 'Backspace' && searchValue === '') {
						selectedValues = selectedValues.slice(0, -1);
						dispatch('remove-option', selectedValues);
					}
				}}
				{placeholder}
				{readonly}
				class:cursor-pointer={cursorPointer}
			/>
		</div>
		<div class="absolute right-0 mr-5 cursor-pointer">
			<slot>
				<Arrow />
			</slot>
		</div>
	</div>
	{#if danger}
		<caption class="text-[#D75870] text-xs">
			{#if dangerMessage}{dangerMessage}{:else}&nbsp;{/if}
		</caption>
	{:else}
		<caption class="text-[#98B3AB] text-xs">
			{#if caption}{caption}{:else}&nbsp;{/if}
		</caption>
	{/if}
</div>

<style type="postcss">
	.input-selected {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ecefff;
	}
	.input-danger {
		@apply border-[#D75870];
	}
	.input-danger-focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ffecec;
	}
</style>
