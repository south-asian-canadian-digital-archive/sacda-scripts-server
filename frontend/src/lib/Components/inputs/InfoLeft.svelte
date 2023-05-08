<script lang="ts">
	import Arrow from '../../Icons/Arrow.svelte';
	import { createEventDispatcher } from 'svelte';

	export let value: string;
	export let label = '';
	export let caption = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	const dispatch = createEventDispatcher();

	function handleSubmit() {
		dispatch('change', value);
	}
</script>

<div class="flex flex-col items-start gap-2 w-full">
	<label class="text-[#47675B] font-medium text-sm" for="">
		{#if label}{label}{:else}&nbsp;{/if}
	</label>
	<div class="flex flex-row gap-0 items-center min-h-[54px]">
		<div
			class="text min-w-[70px] border border-r-0 rounded-r-none border-[#D0DDD7] rounded-14 p-4 text-[#66857D] text-center items-center"
		>
			<slot>
				<div class="flex flex-row justify-center items-center gap-1">
					<span>Text</span>
					<span><Arrow /></span>
				</div>
			</slot>
		</div>

		<input
			type="text"
			class="input-selected z-10 w-full min-h-[54px] border rounded-l-none border-[#D0DDD7] rounded-14 p-4 placeholder:text-[#98B3AB] text-[#47675B] outline-none ease-out duration-100"
			class:input-danger={danger}
			bind:value
			on:keydown={(event) => {
				if (event.key === 'Enter') {
					handleSubmit();
				}
			}}
			{placeholder}
		/>
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
	.input-selected:focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ecefff;
	}
	.input-danger {
		@apply border-[#D75870];
	}
	.input-danger:focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 4px #ffecec;
	}

	.text {
		background: linear-gradient(180deg, #fbfefd 0%, #f8fdfb 100%);
	}
</style>
