<script lang="ts">
	import Calendar from '../../Icons/Calendar.svelte';
	import { clickOutside } from '../../../utils/clickOutside';
	import { createEventDispatcher } from 'svelte';

	export let value: string;
	export let label = '';
	export let caption = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';
	export let inputFocused = false;

	const dispatch = createEventDispatcher();

	function handleSubmit() {
		dispatch('change', value);
	}
</script>

<div class="flex flex-col items-start gap-2 w-full">
	<label class="text-[#47675B] font-medium text-sm" for="">
		{#if label}{label}{:else}&nbsp;{/if}
	</label>
	<div class="flex flex-row gap-0 items-center min-h-[54px] w-full">
		<input
			type="text"
			class="input-selected z-10 w-full min-h-[54px] border rounded-r-none border-[#D0DDD7] rounded-14 p-4 placeholder:text-[#98B3AB] placeholder:text-sm text-[#47675B] outline-none ease-out duration-100"
			class:input-danger={danger}
			class:input-focus={inputFocused}
			bind:value
			on:keydown={(event) => {
				if (event.key === 'Enter') {
					handleSubmit();
				}
			}}
			{placeholder}
		/>
		<div
			class="min-w-[50px] border border-l-0 rounded-l-none border-[#D0DDD7] rounded-14 p-4 text-[#66857D] flex justify-center items-center cursor-pointer"
			on:keydown
			on:click={() => {
				dispatch('icon-click');
			}}
		>
			<slot>
				<Calendar />
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
	.input-selected:focus,
	.input-focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ecefff;
	}
	.input-danger {
		@apply border-[#D75870];
	}
	.input-danger:focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ffecec;
	}

	/* .text {
		background: linear-gradient(180deg, #fbfefd 0%, #f8fdfb 100%);
	} */
</style>
