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
		@apply text-[#21252929] cursor-not-allowed;
	}
	.button {
		@apply hover:bg-[#F2F7F5] border hover:border-[#EAF0ED] border-white text-[#47675B];
	}
	.button:focus {
		transition: box-shadow 0.3s ease-in-out;
		box-shadow: 0px 0px 0px 4px #f5f5f5;
	}
</style>
