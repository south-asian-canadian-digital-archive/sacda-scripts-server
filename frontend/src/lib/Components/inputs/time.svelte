<script lang="ts">
	import IconRight from './IconRight.svelte';

	export let label = '';
	export let caption = '';
	export let value = '';
	export let placeholder = 'Enter here';
	export let danger: boolean = false;
	export let dangerMessage: string = '';

	let timeValue: string = '';
	let timeSelected: 'AM' | 'PM' = 'AM';

	const validateTime = () => {
		if (timeValue) {
			if (/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/.test(timeValue)) {
				value = `${value} ${timeSelected}`;
				danger = false;
				dangerMessage = '';
			} else {
				danger = true;
				dangerMessage = 'Invalid time format';
			}
		} else {
			danger = false;
			dangerMessage = '';
		}
	};

	$: {
		timeValue;
		validateTime();
	}

	function handleSubmit() {
		validateTime();
	}
</script>

<IconRight
	bind:label
	bind:caption
	bind:value={timeValue}
	bind:placeholder
	bind:danger
	bind:dangerMessage
>
	<div class="flex flex-col justify-center items-center text-sm text-[#98B3AB]">
		<span
			class="cursor-pointer"
			class:time-selected={timeSelected === 'AM'}
			on:click={() => {
				timeSelected = 'AM';
			}}
			on:keydown
		>
			AM
		</span>
		<span
			class="cursor-pointer"
			class:time-selected={timeSelected === 'PM'}
			on:click={() => {
				timeSelected = 'PM';
			}}
			on:keydown
		>
			PM
		</span>
	</div>
</IconRight>

<style type="postcss">
	.time-selected {
		@apply text-[#47675B] font-semibold ease-in-out duration-200;
	}
</style>
