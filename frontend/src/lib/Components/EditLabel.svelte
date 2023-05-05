<script>
	import Close from '$lib/Icons/updates/Close.svelte';
	import Edit from '$lib/Icons/updates/Edit.svelte';
	import TickCircle from '$lib/Icons/updates/tick-circle.svelte';
	import { createEventDispatcher } from 'svelte';
	import { fade, fly } from 'svelte/transition';

	export let label = '';

	let editMode = false;
	let editingLabel = label;
	let dispatch = createEventDispatcher();
</script>

{#key label}
	<div class="flex flex-row items-center gap-1">
		{#if !editMode}
			<span>
				{#if label}{label}{:else}&nbsp;{/if}
			</span>
			<span
				in:fly
				class="pt-0.5 cursor-pointer"
				on:click={() => {
					editMode = true;
				}}
				on:keydown
			>
				<Edit />
			</span>
		{:else}
			<span
				contenteditable="true"
				class="outline-none"
				bind:innerHTML={editingLabel}
				on:keydown={(e) => {
					if (e.key === 'Enter') {
						label = editingLabel;
						dispatch('labelChange');
						editMode = false;
					}
				}}
			/>

			<div
				in:fly
				class="text-[#D0DDD7] bg-[#F2F7F5] rounded h-5 w-12 flex flex-row justify-evenly text-center items-center"
			>
				<span
					on:click={() => {
						editingLabel = label;
						editMode = false;
					}}
					on:keydown
					class="cursor-pointer"
				>
					<Close />
				</span>
				|
				<span
					class="cursor-pointer"
					on:keydown
					on:click={() => {
						label = editingLabel;
						dispatch('labelChange');
						editMode = false;
					}}
				>
					<TickCircle />
				</span>
			</div>
		{/if}
	</div>
{/key}
