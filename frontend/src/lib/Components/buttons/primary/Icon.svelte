<script lang="ts">
	import Activity from '../../../Icons/activity.svelte';

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
			<Activity />
		</span>
	</slot>
</button>

<style type="postcss">
	.xs {
		@apply p-2 font-medium text-xs text-white rounded-lg;
	}

	.sm {
		@apply p-2.5 font-medium text-sm text-white rounded-lg;
	}

	.md {
		@apply p-3 font-medium text-sm text-white rounded-[11px];
	}

	.lg {
		@apply p-[18px] font-semibold text-base text-white rounded-14;
	}

	.disabled {
		@apply bg-[#BAE5D1] cursor-not-allowed;
	}
	.button {
		background: linear-gradient(125.27deg, #0f9d58 24.26%, #037a4f 205.65%);
		box-shadow: 0px 4px 12px rgba(15, 157, 88, 0.24), inset 0px 0.5px 0px rgba(255, 255, 255, 0.5);
		transition: box-shadow 0.5s ease-in-out;
	}
	.button:hover {
		background: linear-gradient(125.27deg, #148944 24.26%, #005227 205.65%);
	}
	.button:focus {
		box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.07), 0px 0px 0px 3px #b4f3d1;
	}
</style>
