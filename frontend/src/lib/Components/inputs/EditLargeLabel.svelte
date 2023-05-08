<script lang="ts">
	import Edit from '../../Icons/Edit.svelte';
	import { createEventDispatcher } from 'svelte';
	import EditLabel from '../EditLabel.svelte';

	export let value: string;
	export let label = '';
	export let caption = '';
	export let maxLength = 250;
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	let editMode = false;

	const dispatch = createEventDispatcher();

	function handleSubmit() {
		dispatch('submit', value);
	}
</script>

<div class="flex flex-col items-start gap-2 w-full">
	<label class="text-[#47675B] font-medium text-sm flex flex-row justify-between w-full" for="">
		<span>
			{#if label}
				<EditLabel
					bind:label
					on:labelChange={() => {
						dispatch('labelChange');
					}}
				/>
			{:else}&nbsp;{/if}
		</span>

		<span class="text-[#98B3AB] text-xs" class:danger-wordcount={danger}>
			{#if maxLength}
				{value.length}/{maxLength}
			{/if}
		</span>
	</label>
	<div class="relative w-full">
		<textarea
			class="input-style min-h-[70px] w-full border border-[#D0DDD7] rounded-14 p-4 placeholder:text-[#98B3AB] text-[#47675B] outline-none ease-out duration-100"
			class:input-danger={danger}
			bind:value
			on:keydown={(event) => {
				if (event.key === 'Enter') {
					handleSubmit();
				}
			}}
			{placeholder}
			maxlength={maxLength}
		/>
		<div class="absolute right-1 bottom-3">
			<svg width="9" height="9" viewBox="0 0 9 9" fill="none" xmlns="http://www.w3.org/2000/svg">
				<path d="M8 5L5 8M8 1L1 8" stroke="#212529" stroke-opacity="0.16" stroke-linecap="square" />
			</svg>
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
	::-webkit-resizer {
		display: none;
	}

	.input-style:focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ecefff;
	}
	.input-danger {
		@apply border-[#D75870];
	}
	.input-danger:focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ffecec;
	}
	.danger-wordcount {
		@apply text-[#D75870];
	}
</style>
