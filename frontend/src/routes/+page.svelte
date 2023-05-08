<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import Dropdown from '../lib/Components/dropdowns/Default.svelte';
	import Input from '../lib/Components/inputs/Main.svelte';

	let metadataType: 'File' | 'Link' = 'File';
	let language: 'English' | 'Hindi' | 'Punjabi' | 'Japanese' = 'English';
	let outputType: 'PDF' | 'PDF/A' = 'PDF';

	let metadataLink: string = '';
	let metadataFile: FileList | null = null;
	let collectionFile: FileList | null = null;
	let singleDocFile: FileList | null = null;

	const uploadSingle = () => {

	}

</script>

<main class="flex flex-col gap-14 h-screen py-20 items-center justify-center overflow-y-auto">
	<form class="container">
		<h1>SACDA SINGLE DOC OCR</h1>

		<div class="input-container">
			<Dropdown
				label="Lanuage"
				caption=""
				bind:value={language}
				options={['English', 'Hindi', 'Punjabi', 'Japanese']}
			/>
			<Dropdown label="Output Type" caption="" bind:value={outputType} options={['PDF', 'PDF/A']} />
			<FileUpload
				label="File upload"
				caption="supported file formats pdf, jpg, jpeg"
				bind:files={singleDocFile}
			/>
		</div>
	</form>

	<div class="container">
		<h1>SACDA COLLECTION OCR</h1>

		<div class="input-container">
			<Dropdown
				label="Metadata Type"
				bind:value={metadataType}
				caption=""
				options={['File', 'Link']}
			/>
			{#if metadataType === 'Link'}
				<Input bind:value={metadataLink} label="Link" caption="Enter link" />
			{:else}
				<FileUpload
					bind:files={metadataFile}
					label="Metadata file"
					caption="supported file formats csv"
				/>
			{/if}
			<FileUpload
				bind:files={collectionFile}
				label="Collection zip"
				caption="supported file formats zip"
			/>
		</div>
	</div>
</main>

<style type="postcss">
	h1 {
		@apply text-4xl font-bold text-[#212529];
	}
	.container {
		@apply flex flex-col gap-10 h-80 w-1/2 p-10 pb-8 rounded-2xl border border-[#21252914];

		box-shadow: 0px 4px 24px rgba(8, 5, 46, 0.04);
	}
	.input-container {
		@apply flex flex-row w-full gap-6;
	}
</style>
