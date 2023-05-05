<script lang="ts">
	export let label = '';
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
			{label}
		</span>
	</slot>
</button>

<style type="postcss">
	.xs {
		@apply py-2 px-3.5 font-medium text-xs rounded-lg;
	}

	.sm {
		@apply py-2.5 px-4 font-medium text-sm rounded-lg;
	}

	.md {
		@apply py-3 px-5 font-medium text-sm rounded-[11px];
	}

	.lg {
		@apply py-[17px] px-7 font-semibold text-base rounded-14;
	}

	.disabled {
		@apply bg-white cursor-not-allowed text-[#21252929] border border-[#F2F7F5];
	}
	.button {
		@apply text-[#47675B] border-[#D0DDD7] border;
		transition: box-shadow 0.3s ease-in-out;
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
