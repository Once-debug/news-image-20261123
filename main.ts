#!/usr/bin/env node
// news-image-20261123 — entrypoint for "Sum up 23 November's world news in one image".
//
// The broadsheet is typeset ahead of time by tools/make_image.py (Python +
// Pillow) and the finished page is committed beside this file as entry.png.
// Grading runs offline, twice, and both runs must agree byte for byte, so
// this program does the smallest honest job: it checks the committed page
// against the gate (PNG signature, 1024x1024, at most 1 MiB) and copies it
// into the output directory untouched.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const pageFile = join(root, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

if (!existsSync(pageFile)) {
  throw new Error("entry.png is missing from the repository root");
}

const head = readFileSync(pageFile).subarray(0, 24);
const PNG_SIG = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
if (!PNG_SIG.every((b, i) => head[i] === b)) {
  throw new Error("entry.png does not start with the PNG signature");
}
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

const size = statSync(pageFile).size;
if (size > 1_048_576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(pageFile, dest);
console.log(`entry.png -> ${dest} (${width}x${height}, ${size} bytes)`);
