<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import EditLabel from '../EditLabel.svelte';

	export let value;
	export let label = '';
	export let caption = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	const dispatch = createEventDispatcher();

	function handleSubmit() {
		dispatch('submit', value);
	}
</script>

<div class="flex flex-col items-start gap-2 w-full">
	<label class="text-[#47675B] font-medium text-sm" for="">
		{#if label}
			<EditLabel
				bind:label
				on:labelChange={() => {
					dispatch('labelChange');
				}}
			/>
		{:else}&nbsp;{/if}
	</label>
	<input
		type="text"
		class="input-selected w-full min-h-[54px] border border-[#D0DDD7] rounded-14 p-4 placeholder:text-[#98B3AB] text-[#47675B] outline-none ease-out duration-100"
		class:input-danger={danger}
		bind:value
		on:keydown={(event) => {
			if (event.key === 'Enter') {
				handleSubmit();
			}
		}}
		{placeholder}
	/>
	{#if danger}
		<caption class="text-[#D75870] text-xs">
			{#if dangerMessage}{dangerMessage}{:else}&nbsp;{/if}
		</caption>
	{:else}
		<caption class="text-[#66857D] text-xs">
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
</style>
