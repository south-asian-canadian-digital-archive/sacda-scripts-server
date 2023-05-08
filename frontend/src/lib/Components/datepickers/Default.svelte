<script lang="ts">
	import { writable } from 'svelte/store';
	import { createEventDispatcher } from 'svelte';
	import Arrow from '$lib/Icons/Arrow.svelte';
	import { fly } from 'svelte/transition';

	export let today = new Date(); // Date
	export let year = today.getFullYear();
	export let month = today.getMonth(); // Jan
	export let offset = 0; // Sun

	/**
	 * @type {Date | null}
	 */
	 export let selectedDate = null;

	export let labels = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
	export let months = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];

	const dispatch = createEventDispatcher();

	$: today_month = today && today.getMonth();
	$: today_year = today && today.getFullYear();
	$: today_day = today && today.getDate();

	let yearMode = writable(false);
	const yearGap = 300;
	const generateInitialYears = (year_ = year) => {
		const years = [];

		for (let i = year_ - yearGap; i <= year_ + yearGap; i++) {
			years.push(i);
		}
		return years;
	};
	let initYears = generateInitialYears();
	let yd = null;

	yearMode.subscribe((val) => {
		setTimeout(() => {
			if (yd) {
				yd.scrollTop = ((year - initYears[0]) / 4) * 45;
				yd = yd;
			}
		}, 100);
	});

	const generateNextYears = () => {
		let temp = [];

		for (
			let i = initYears[initYears.length - 1];
			i <= initYears[initYears.length - 1] + yearGap;
			i++
		) {
			temp.push(i);
		}

		initYears = [...initYears, ...temp];
	};
	const generatePrevYears = () => {
		let temp = [];

		for (let i = initYears[0] - yearGap; i < initYears[0]; i++) {
			temp.push(i);
		}

		initYears = [...temp, ...initYears];
	};

	const calendarize = (target, offset) => {
		var i = 0,
			j = 0,
			week,
			out = [],
			date = new Date(target || new Date());
		var year = date.getFullYear(),
			month = date.getMonth();

		// day index (of week) for 1st of month
		var first = new Date(year, month, 1 - (offset | 0)).getDay();

		// how many days there are in this month
		var days = new Date(year, month + 1, 0).getDate();

		while (i < days) {
			for (j = 0, week = Array(7); j < 7; ) {
				while (j < first) week[j++] = 0;
				week[j++] = ++i > days ? 0 : i;
				first = 0;
			}
			out.push(week);
		}

		return out;
	};

	$: prev = calendarize(new Date(year, month - 1), offset);
	$: current = calendarize(new Date(year, month), offset);
	$: next = calendarize(new Date(year, month + 1), offset);

	const toPrev = () => {
		[current, next] = [prev, current];

		if (--month < 0) {
			month = 11;
			year--;
		}

		prev = calendarize(new Date(year, month - 1), offset);
	};

	const toNext = () => {
		[prev, current] = [current, next];

		if (++month > 11) {
			month = 0;
			year++;
		}

		next = calendarize(new Date(year, month + 1), offset);
	};

	const isToday = (day) => {
		return today && today_year === year && today_month === month && today_day === day;
	};

	const isSelected = (day) => {
		return (
			selectedDate &&
			selectedDate.getFullYear() === year &&
			selectedDate.getMonth() === month &&
			selectedDate.getDate() === day
		);
	};

	const selectDate = (day) => {
		let old = selectedDate;

		selectedDate = new Date(year, month, day);

		dispatch('select', { old: old, new: selectedDate });
	};
</script>

<div class="wrapper overflow-clip">
	<div class="flex flex-row items-center justify-between p-4">
		<div class="arrow rotate-90 cursor-pointer" on:click={toPrev} on:keydown>
			<Arrow size={10} />
		</div>

		<div class="flex flex-row items-center gap-3">
			<span class="text-[#47675B] font-semibold text-xs">{months[month]}, {year}</span>
			<span
				class="cursor-pointer select-none"
				class:rotate-180={$yearMode}
				on:keydown
				on:click={() => {
					$yearMode = !$yearMode;
				}}
			>
				<Arrow size={12} />
			</span>
		</div>

		<div class="arrow -rotate-90 cursor-pointer" on:click={toNext} on:keydown>
			<Arrow size={10} />
		</div>
	</div>

	{#key [selectedDate, year]}
		<div
			class="grid grid-cols-7 gap-1 text-center -ml-2 p-4 px-5 pt-2 border-t border-[#EAF0ED]"
			class:hidden={$yearMode}
		>
			{#each labels as txt, idx (idx)}
				<span class="label">{labels[(idx + offset) % 7]}</span>
			{/each}

			{#each { length: 6 } as w, idxw (idxw)}
				{#if current[idxw]}
					{#each { length: 7 } as d, idxd (idxd)}
						{#if current[idxw][idxd] != 0}
							<span
								class="date"
								class:selected={isSelected(current[idxw][idxd])}
								on:keydown
								on:click={() => selectDate(current[idxw][idxd])}
							>
								{current[idxw][idxd]}
							</span>
						{:else if idxw < 1}
							<span class="date other" on:keydown on:click={() => selectDate(current[idxw][idxd])}
								>{prev[prev.length - 1][idxd]}</span
							>
						{:else}
							<span class="date other" on:keydown on:click={() => selectDate(current[idxw][idxd])}
								>{next[0][idxd]}</span
							>
						{/if}
					{/each}
				{/if}
			{/each}
		</div>
	{/key}
	{#if $yearMode}
		<div
			in:fly={{ opacity: 1, y: 500 }}
			class="max-h-[285px] relative overflow-y-auto grid grid-cols-4 gap-1 text-center p-4 px-5 pt-2 border-t border-[#EAF0ED]"
			bind:this={yd}
			on:scroll={(e) => {
				if (e.currentTarget.scrollTop >= e.currentTarget.scrollHeight - 500) {
					generateNextYears();
				}

				if (e.currentTarget.scrollTop <= 200) {
					generatePrevYears();
				}
			}}
			class:hidden={!$yearMode}
		>
			{#each initYears as y, idxy (idxy)}
				<span
					class="year relative"
					class:selected={year === y}
					on:keydown
					on:click={() => {
						year = y;
						$yearMode = false;
					}}
				>
					{y}
				</span>
			{/each}
		</div>
	{/if}
</div>

<style type="postcss">
	.arrow {
		@apply select-none w-9 h-9 border border-[#D0DDD7] rounded-lg flex items-center justify-center;
		box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.07);
	}
	.wrapper {
		@apply border border-[#EAF0ED] rounded-2xl;
		box-shadow: 0px 12px 16px -4px rgba(16, 24, 40, 0.04), 0px 4px 6px -2px rgba(16, 24, 40, 0.02);
	}

	.label {
		@apply text-[#98B3AB] w-10 h-10 text-sm font-semibold flex justify-center items-center;
	}

	.date {
		@apply text-[#47675B] w-10 h-10 text-sm flex justify-center cursor-pointer items-center font-semibold hover:bg-[#F9FBFB] border border-transparent rounded-lg hover:border-[#EAF0ED];
	}

	.year {
		@apply text-[#47675B] px-[13px] py-[10px] text-sm flex justify-center cursor-pointer items-center font-semibold hover:bg-[#F9FBFB] border border-transparent rounded-lg hover:border-[#EAF0ED];
	}

	.date.selected,
	.year.selected {
		@apply bg-[#0F9D58] text-white z-10 border-none;
	}

	.date.other {
		@apply text-[#98B3AB];
	}
</style>
