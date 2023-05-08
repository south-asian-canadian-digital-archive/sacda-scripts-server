<script lang="ts">
	import Close from '$lib/Icons/Close.svelte';
	import DocumentUpload from '$lib/Icons/document-upload.svelte';
	import PlayCircle from '$lib/Icons/play-circle.svelte';
	import { createEventDispatcher } from 'svelte';

	export let files: FileList | null;
	export let label = '';
	export let caption = '';

	export let danger: boolean = false;
	export let dangerMessage: string = '';

	let input: HTMLInputElement;

	// $: console.log(files);

	const dispatch = createEventDispatcher();
</script>

<div class="flex flex-col items-start gap-2 w-full">
	<label class="text-[#47675B] font-medium text-sm" for="">
		{#if label}{label}{:else}&nbsp;{/if}
	</label>
	<div
		class="input-selected flex flex-row gap-3 items-center justify-center w-full text-[#66857D] min-h-[54px] border border-dashed border-[#D0DDD7] rounded-14 p-4 outline-none ease-out duration-100 cursor-pointer select-none"
		class:input-danger={danger}
		class:files
		on:click={() => {
			input?.click();
		}}
		on:keydown
		on:dragover={(e) => {
			// console.log('dragover');
			e.preventDefault();
		}}
		on:drop={(e) => {
			files = e.dataTransfer?.files || null;
			dispatch('change', files);

			e.preventDefault();
		}}
	>
		{#if files}
			<div class="flex flex-row justify-between w-full items-center">
				<span class="flex flex-row items-center gap-1 text-[#1D3932]">
					<PlayCircle />
					{files[0].name}
				</span>
				<span
					on:click|stopPropagation={() => {
						files = null;
					}}
					on:keydown
				>
					<Close color="#47675B" size="20" />
				</span>
			</div>
		{:else}
			<DocumentUpload />
			<span>Upload file</span>
		{/if}
		<input type="file" bind:files hidden bind:this={input} />
	</div>
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
	.files {
		@apply border-solid border-[#D0DDD7];
	}
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
