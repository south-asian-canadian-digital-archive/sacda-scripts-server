<script lang="ts">
	import Activity from '$lib/Icons/activity.svelte';
	import Default from './Default.svelte';

	export let size: 'xs' | 'sm' | 'md' | 'lg' = 'md';
	export let label: string = '';
	export let disabled: boolean = false;
</script>

<Default bind:size bind:disabled>
	<div class="flex flex-row justify-center items-center gap-2">
		<slot>
			<Activity color="#47675B" />
		</slot>
		<span>{label}</span>
	</div>
</Default>
