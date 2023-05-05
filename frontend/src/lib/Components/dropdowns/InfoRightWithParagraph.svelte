<script lang="ts">
	import { slide } from 'svelte/transition';
	import InfoRightDefault from './InfoRight.svelte';

	export let label;
	export let caption;
	export let value;
	export let placeholder = '';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	export let defaultValue: {
		icon: string;
		title: string;
		description: string;
		value: string;
	};
	export let infoValue: {
		icon: string;
		title: string;
		description: string;
		value: string;
	};
	export let options: {
		icon: string;
		title: string;
		description: string;
		value: string;
	}[] = [];
	export let singleValueBuffer = '';
	export let deafultValueBuffer = defaultValue?.value || options[0]?.value || 'AM';

	let dropdownOpen = false;
	let inputFocused = false;
</script>

<InfoRightDefault
	bind:label
	bind:caption
	bind:value
	bind:placeholder
	bind:danger
	bind:dangerMessage
	bind:dropdownOpen
	bind:inputFocused
	bind:infoValue={singleValueBuffer}
	bind:defaultValue={deafultValueBuffer}
>
	{#each options as option}
		<div
			class="flex flex-row items-center justify-start gap-3 px-4 py-3 cursor-pointer border-y hover:border-[#F2F4F7] border-white"
			on:keydown
			on:click|stopPropagation={() => {
				dropdownOpen = false;
				inputFocused = false;

				infoValue = option;
				singleValueBuffer = option.value;
			}}
			transition:slide={{ duration: 100 }}
		>
			{#if option.icon}
				<div class="rounded-full object-cover w-10 h-10 mx-2">
					<img src={option.icon} alt="" />
				</div>
				<!-- {:else}
					<div class="w-10 h-10 rounded-full bg-[#21252914]" /> -->
			{/if}
			<div class="flex flex-col justify-evenly">
				<span class="text-[#47675B] text-sm font-semibold">{option.title}</span>
				<span class="text-[#98B3AB] text-sm font-normal">{option.description || ''}</span>
			</div>
		</div>
	{/each}
</InfoRightDefault>
