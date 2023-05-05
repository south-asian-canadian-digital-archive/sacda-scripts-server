<script lang="ts">
	import Arrow from '$lib/Icons/updates/Arrow.svelte';
	import { writable } from 'svelte/store';
	import { fly } from 'svelte/transition';

	export let today = new Date(); // Date
	export let year = today.getFullYear();
	export let month = today.getMonth(); // Jan
	export let offset = 0; // Sun

	export let startDate: Date = null;
	export let endDate: Date = null;

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
				yd.scrollTop = (Math.ceil(year - initYears[0]) / 4) * 45;
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
	$: currentLeft = calendarize(new Date(year, month), offset);
	$: currentRight = calendarize(new Date(year, month + 1), offset);
	$: next = calendarize(new Date(year, month + 2), offset);

	const toPrev = () => {
		[currentLeft, currentRight, next] = [prev, currentLeft, currentRight];

		if (--month < 0) {
			month = 11;
			year--;
		}

		prev = calendarize(new Date(year, month - 1), offset);
	};

	const toNext = () => {
		[prev, currentLeft, currentRight] = [currentLeft, currentRight, next];

		if (++month > 11) {
			month = 0;
			year++;
		}

		next = calendarize(new Date(year, month + 2), offset);
	};

	const isToday = (day) => {
		return today && today_year === year && today_month === month && today_day === day;
	};

	const isSelected = (day, month, endDate) => {
		return (
			(startDate &&
				startDate.getFullYear() === year &&
				startDate.getMonth() === month &&
				startDate.getDate() === day) ||
			(endDate &&
				endDate.getFullYear() === year &&
				endDate.getMonth() === month &&
				endDate.getDate() === day)
		);
	};

	const isSameDate = (date1, date2) => {
		return (
			date1.getFullYear() === date2.getFullYear() &&
			date1.getMonth() === date2.getMonth() &&
			date1.getDate() === date2.getDate()
		);
	};

	export let selectedRange: Date[] = [];
	const selectRange = (day, month) => {
		if (!startDate || endDate) {
			startDate = new Date(year, month, day);
			endDate = null;
			selectedRange = [];
		} else {
			let temp = new Date(year, month, day);
			if (startDate < temp) endDate = temp;
			else startDate = temp;
		}
	};

	$: hoveringEndDate = null;
	const dateMouseIn = (day, month) => {
		if (!startDate) return;
		hoveringEndDate = new Date(year, month, day);
	};
	const dateMouseOut = () => {
		hoveringEndDate = null;
	};

	const isInRange = (day, month_, hoveringEndDate) => {
		if (!(startDate && (hoveringEndDate || endDate))) return false;

		day = new Date(year, month_, day);

		if (day > startDate && day < (endDate ? endDate : hoveringEndDate)) {
			if (!selectedRange.find((d) => isSameDate(d, day))) {
				selectedRange.push(day);
			}
		}

		return day > startDate && day < (endDate ? endDate : hoveringEndDate);
	};
</script>

<div class="wrapper-big flex flex-row">
	<div class="wrapper-left overflow-clip">
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

			<!-- <div class="arrow -rotate-90 cursor-pointer" on:click={toNext} on:keydown>
				<Arrow size={10} />
			</div> -->
			<div class="w-9 h-9" />
		</div>

		{#key startDate}
			<div
				class="grid grid-cols-7 gap-1 text-center -ml-2 p-4 px-5 pt-2 border-t border-[#EAF0ED]"
				class:hidden={$yearMode}
			>
				{#each labels as txt, idx (idx)}
					<span class="label">{labels[(idx + offset) % 7]}</span>
				{/each}

				{#each { length: 6 } as w, idxw (idxw)}
					{#if currentLeft[idxw]}
						{#each { length: 7 } as d, idxd (idxd)}
							{#if currentLeft[idxw][idxd] != 0}
								<!-- class:today={isToday(current[idxw][idxd])} -->
								<span
									class="date"
									class:selected={isSelected(currentLeft[idxw][idxd], month, endDate)}
									class:in-range={isInRange(currentLeft[idxw][idxd], month, hoveringEndDate)}
									class:in-range-right={isInRange(
										currentLeft[idxw][idxd],
										month,
										hoveringEndDate
									) && !currentLeft[idxw][idxd + 1]}
									class:in-range-left={isInRange(currentLeft[idxw][idxd], month, hoveringEndDate) &&
										!currentLeft[idxw][idxd - 1]}
									on:keydown
									on:click={() => selectRange(currentLeft[idxw][idxd], month)}
									on:mouseenter={() => {
										dateMouseIn(currentLeft[idxw][idxd], month);
									}}
									on:mouseout={dateMouseOut}
									on:blur
								>
									{currentLeft[idxw][idxd]}
								</span>
							{:else if idxw < 1}
								<span class="date other">{prev[prev.length - 1][idxd]}</span>
								<!-- class:selected={isSelected(prev[prev.length - 1][idxd], month - 1, endDate)}
									class:in-range={isInRange(
										prev[prev.length - 1][idxd],
										month - 1,
										hoveringEndDate
									)}
									class:in-range-right={isInRange(
										prev[prev.length - 1][idxd],
										month - 1,
										hoveringEndDate
									) && idxd === 6}
									class:in-range-left={isInRange(
										prev[prev.length - 1][idxd],
										month - 1,
										hoveringEndDate
									) && idxd === 0}
									on:keydown
									on:click={() => selectRange(prev[prev.length - 1][idxd], month - 1)}
									on:mouseenter={() => {
										dateMouseIn(prev[prev.length - 1][idxd], month - 1);
									}}
									on:mouseout={dateMouseOut}
									on:blur -->
							{:else}
								<span class="date other">{currentRight[0][idxd]}</span>
								<!-- class:selected={isSelected(currentRight[0][idxd], month + 1, endDate)}
								class:in-range={isInRange(currentRight[0][idxd], month + 1, hoveringEndDate)}
								class:in-range-right={isInRange(
									currentRight[0][idxd],
									month + 1,
									hoveringEndDate
								) && idxd === 6}
								class:in-range-left={isInRange(currentRight[0][idxd], month + 1, hoveringEndDate) &&
									idxd === 0}
								on:keydown on:click={() => selectRange(currentRight[0][idxd], month + 1)}
								on:mouseenter={() => {
									dateMouseIn(currentRight[0][idxd], month + 1);
								}}
								on:mouseout={dateMouseOut}
								on:blur -->
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

	<div class="wrapper-right overflow-clip">
		<div class="flex flex-row items-center justify-between p-4">
			<!-- <div class="arrow rotate-90 cursor-pointer" on:click={toPrev} on:keydown>
				<Arrow size={10} />
			</div> -->
			<div class="w-9 h-9" />

			<div class="flex flex-row items-center gap-3">
				<span class="text-[#47675B] font-semibold text-xs">{months[month + 1]}, {year}</span>
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

		<!-- {#if !yearMode} -->
		{#key startDate}
			<div class="grid grid-cols-7 gap-1 text-center -ml-2 p-4 px-5 pt-2 border-t border-[#EAF0ED]">
				{#each labels as txt, idx (idx)}
					<span class="label">{labels[(idx + offset) % 7]}</span>
				{/each}

				{#each { length: 6 } as w, idxw (idxw)}
					{#if currentRight[idxw]}
						{#each { length: 7 } as d, idxd (idxd)}
							{#if currentRight[idxw][idxd] != 0}
								<!-- class:today={isToday(current[idxw][idxd])} -->
								<span
									class="date"
									class:selected={isSelected(currentRight[idxw][idxd], month + 1, endDate)}
									class:in-range={isInRange(currentRight[idxw][idxd], month + 1, hoveringEndDate)}
									class:in-range-right={isInRange(
										currentRight[idxw][idxd],
										month + 1,
										hoveringEndDate
									) && !currentRight[idxw][idxd + 1]}
									class:in-range-left={isInRange(
										currentRight[idxw][idxd],
										month + 1,
										hoveringEndDate
									) && !currentRight[idxw][idxd - 1]}
									on:keydown
									on:click={() => selectRange(currentRight[idxw][idxd], month + 1)}
									on:mouseenter={() => {
										dateMouseIn(currentRight[idxw][idxd], month + 1);
									}}
									on:mouseout={dateMouseOut}
									on:blur
								>
									{currentRight[idxw][idxd]}
								</span>
							{:else if idxw < 1}
								<span class="date other">{currentLeft[currentLeft.length - 1][idxd]}</span>
								<!-- class:selected={isSelected(
									currentLeft[currentLeft.length - 1][idxd],
									month,
									endDate
								)}
								class:in-range={isInRange(
									currentLeft[currentLeft.length - 1][idxd],
									month,
									hoveringEndDate
								)}
								class:in-range-right={isInRange(
									currentLeft[currentLeft.length - 1][idxd],
									month,
									hoveringEndDate
								) && idxd === 6}
								class:in-range-left={isInRange(
									currentLeft[currentLeft.length - 1][idxd],
									month,
									hoveringEndDate
								) && idxd === 0}
								on:keydown on:click={() =>
									selectRange(currentLeft[currentLeft.length - 1][idxd], month)}
								on:mouseenter={() => {
									dateMouseIn(currentLeft[currentLeft.length - 1][idxd], month);
								}}
								on:mouseout={dateMouseOut}
								on:blur -->
							{:else}
								<span class="date other">{next[0][idxd]}</span>
								<!-- class:selected={isSelected(next[0][idxd], month + 2, endDate)}
									class:in-range={isInRange(next[0][idxd], month + 2, hoveringEndDate)}
									class:in-range-right={isInRange(next[0][idxd], month + 2, hoveringEndDate) &&
										idxd === 6}
									class:in-range-left={isInRange(next[0][idxd], month + 2, hoveringEndDate) &&
										idxd === 0}
									on:keydown
									on:click={() => selectRange(next[0][idxd], month + 2)}
									on:mouseenter={() => {
										dateMouseIn(next[0][idxd], month + 2);
									}}
									on:mouseout={dateMouseOut}
									on:blur -->
							{/if}
						{/each}
					{/if}
				{/each}
			</div>
		{/key}
	</div>
</div>

<style type="postcss">
	.arrow {
		@apply select-none w-9 h-9 border border-[#D0DDD7] rounded-lg flex items-center justify-center;
		box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.07);
	}

	.wrapper-big {
		@apply rounded-2xl;
		box-shadow: 0px 12px 16px -4px rgba(16, 24, 40, 0.04), 0px 4px 6px -2px rgba(16, 24, 40, 0.02);
	}

	.wrapper-left {
		@apply rounded-l-2xl border border-[#EAF0ED] w-[273px];
	}
	.wrapper-right {
		@apply rounded-r-2xl border-l-0 border border-[#EAF0ED] w-[273px];
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
	.in-range {
		@apply bg-[#f3f7f5] rounded-none hover:rounded-lg hover:z-10;
	}
	.in-range-right {
		@apply bg-[#f3f7f5] rounded-r-lg hover:z-10;
	}
	.in-range-left {
		@apply bg-[#f3f7f5] rounded-l-lg rounded-lg hover:z-10;
	}
	.other {
		@apply text-[#98B3AB];
		visibility: hidden;
	}
</style>
