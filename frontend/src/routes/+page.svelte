<script lang="ts">
	import FileUpload from '$lib/Components/FileUpload.svelte';
	import Default from '$lib/Components/buttons/primary/Default.svelte';
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
		console.log(language, outputType, singleDocFile);
	};
	const uploadCollection = () => {};
</script>

<main class="flex flex-col gap-14 h-screen py-20 items-center justify-center overflow-y-auto">
	<form
		action="http://localhost:8000/ocr-files/"
		enctype="multipart/form-data"
		method="post"
		class="container"
	>
		<h1>SACDA SINGLE DOC OCR</h1>

		<div class="input-container">
			<Dropdown
				label="Lanuage"
				caption=""
				name="language"
				bind:value={language}
				options={['English', 'Hindi', 'Punjabi', 'Japanese']}
			/>
			<Dropdown
				label="Output Type"
				caption=""
				name="output_type"
				bind:value={outputType}
				options={['PDF', 'PDF/A']}
			/>
			<FileUpload
				label="File upload"
				caption="supported file formats pdf, jpg, jpeg"
				name="files"
				multiple
				accept="application/pdf, image/jpeg, image/jpg"
				bind:files={singleDocFile}
			/>
		</div>

		<div class="w-full flex flex-row justify-end">
			<Default on:click={uploadSingle}>Upload</Default>
		</div>
	</form>

	<form
		action="http://localhost:8000/ocr-collection/"
		enctype="multipart/form-data"
		method="post"
		class="container"
	>
		<h1>SACDA COLLECTION OCR</h1>

		<div class="input-container">
			<Dropdown
				label="Metadata Type"
				bind:value={metadataType}
				caption=""
				options={['File', 'Link']}
				name="metadata_type"
			/>
			<!-- {#if metadataType === 'Link'} -->
			<span class:hidden={metadataType !== 'Link'} class="w-3/4">
				<Input
					bind:value={metadataLink}
					label="Link"
					caption="Enter link"
					name="metadata_file_link"
				/>
			</span>
			<!-- {:else} -->
			<span class:hidden={metadataType !== 'File'} class="w-3/4">
				<FileUpload
					bind:files={metadataFile}
					label="Metadata file"
					caption="supported file formats csv"
					accept="text/csv"
					name="metadata_file"
				/>
			</span>
			<!-- {/if} -->
			<FileUpload
				bind:files={collectionFile}
				label="Collection zip"
				caption="supported file formats zip"
				accept="application/zip"
				name="collection_zip"
			/>
		</div>

		<div class="w-full flex flex-row justify-end">
			<Default on:click={uploadCollection}>Upload</Default>
		</div>
	</form>
</main>

<style type="postcss">
	h1 {
		@apply text-4xl font-bold text-[#212529];
	}
	.container {
		@apply flex flex-col gap-10 w-1/2 p-10 rounded-2xl border border-[#21252914];

		box-shadow: 0px 4px 24px rgba(8, 5, 46, 0.04);
	}
	.input-container {
		@apply flex flex-row w-full gap-6;
	}
</style>
