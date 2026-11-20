// news-image-20261119 — "THE WORLD IN A DAY", a front-page poster.
//
// The image is the entry: entry.png, sitting beside this file, already
// holds the finished poster. This program's job is to publish it,
// unchanged, as entry.png in the output directory — but only after
// checking that the bytes really are a PNG inside the gate's limits
// (at most 1 MiB, at most 1024x1024 pixels), so a broken or swapped
// image fails loudly here instead of being judged.
//
// The output directory is /output in the grader's container;
// MAKEFUN_OUTPUT_DIR overrides it for local runs:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const BYTE_LIMIT = 1024 * 1024; // the gate's 1 MiB cap
const SIDE_LIMIT = 1024;        // the gate's cap on each side, in pixels

const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function die(reason: string): never {
  console.error(`main.ts: refusing to publish entry.png: ${reason}`);
  process.exit(1);
}

// Read the width and height out of the IHDR chunk, checking the PNG
// signature and the first chunk's layout on the way. Returns null when
// the bytes are not a PNG with a readable header.
function pngSize(bytes: Buffer): { width: number; height: number } | null {
  if (bytes.length < 24) return null;
  for (let i = 0; i < PNG_MAGIC.length; i += 1) {
    if (bytes[i] !== PNG_MAGIC[i]) return null;
  }
  // First chunk must be a 13-byte IHDR: its length sits at offset 8
  // and its type at offset 12, then width and height follow as u32be.
  if (bytes.readUInt32BE(8) !== 13) return null;
  if (bytes.toString('ascii', 12, 16) !== 'IHDR') return null;
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

let poster: Buffer;
try {
  poster = readFileSync(source);
} catch {
  die(`cannot read ${source}`);
}

if (poster.length === 0) die('the file is empty');
if (poster.length > BYTE_LIMIT) {
  die(`${poster.length} bytes exceeds the ${BYTE_LIMIT}-byte limit`);
}
const size = pngSize(poster);
if (size === null) die('the file does not start with a valid PNG header');
if (size.width < 1 || size.height < 1) {
  die(`nonsense dimensions ${size.width}x${size.height}`);
}
if (size.width > SIDE_LIMIT || size.height > SIDE_LIMIT) {
  die(`${size.width}x${size.height} exceeds the ${SIDE_LIMIT}x${SIDE_LIMIT} limit`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, poster);
console.log(`published ${target}: PNG ${size.width}x${size.height}, ${poster.length} bytes`);
