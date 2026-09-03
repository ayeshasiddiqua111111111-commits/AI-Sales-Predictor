import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  webpack: (config) => {
    try {
      const canonicalReact = fs.realpathSync(path.resolve(__dirname, 'node_modules/react'));
      const canonicalReactDom = fs.realpathSync(path.resolve(__dirname, 'node_modules/react-dom'));
      config.resolve.alias = {
        ...config.resolve.alias,
        react: canonicalReact,
        'react-dom': canonicalReactDom,
      };
    } catch (e) {
      // Normal environment without symlinks
    }
    return config;
  },
};

export default nextConfig;
