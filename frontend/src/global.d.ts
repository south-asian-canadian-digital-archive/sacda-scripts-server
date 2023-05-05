/// <reference types="@sveltejs/kit" />

declare namespace svelte.JSX {
	interface HTMLAttributes<T> {
		onclick_outside?: () => void;
		onlongpress?: (e: CustomEventInit) => void;
	}
}
