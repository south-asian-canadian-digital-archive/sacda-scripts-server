import { sveltekit } from '@sveltejs/kit/vite';
import path from 'path';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	resolve: {
		alias: {
			$stores: path.resolve('./src/stores'),
			$styles: path.resolve('./src/styles'),
			$utils: path.resolve('./src/utils'),
			$components: path.resolve('./src/lib/Components'),
			$pages: path.resolve('./src/lib/Pages'),
			$icons: path.resolve('./src/lib/Icons'),
			$constants: path.resolve('./src/lib/constants')
		}
	},
	server: {
		port: 3000,
		fs: {
			allow: ['..']
		}
	}
};

export default config;
