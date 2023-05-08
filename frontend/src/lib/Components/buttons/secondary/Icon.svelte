<script lang="ts">
	import Activity from '$lib/Icons/activity.svelte';

	export let disabled: boolean = false;
	export let size: 'xs' | 'sm' | 'md' | 'lg' = 'md';
</script>

<button
	on:keydown
	on:click
	{disabled}
	class:disabled
	class:button={!disabled}
	class:xs={size === 'xs'}
	class:sm={size === 'sm'}
	class:md={size === 'md'}
	class:lg={size === 'lg'}
>
	<slot>
		<span>
			<Activity color="#47675B" />
		</span>
	</slot>
</button>

<style type="postcss">
	.xs {
		@apply p-2 font-medium text-xs rounded-lg;
	}

	.sm {
		@apply p-2.5 font-medium text-sm rounded-lg;
	}

	.md {
		@apply p-3 font-medium text-sm rounded-[11px];
	}

	.lg {
		@apply p-[18px] font-semibold text-base rounded-14;
	}

	.disabled {
		@apply bg-white cursor-not-allowed border border-[#F2F7F5] text-[#21252929];
	}
	.button {
		@apply text-[#47675B] border-[#D0DDD7] border;
		transition: box-shadow 0.5s ease-in-out;
	}
	.button:hover {
		background: linear-gradient(180deg, #ffffff 0%, #f1f1f1 100%);
		box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.05);
	}
	.button:focus {
		@apply bg-white;
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 3px #f5f5f5;
	}
</style>
