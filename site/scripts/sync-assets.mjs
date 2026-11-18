// Copies brand assets from the repo's assets/ folder into public/brand/ before every build.
// assets/ stays the single source of truth; public/brand/ is generated and git-ignored.
import { cpSync, rmSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repo = join(here, '..', '..');
const dest = join(here, '..', 'public', 'brand');

rmSync(dest, { recursive: true, force: true });
mkdirSync(dest, { recursive: true });
for (const dir of ['logo', 'packaging', 'characters', 'renders']) {
  cpSync(join(repo, 'assets', dir), join(dest, dir), { recursive: true });
}
cpSync(join(repo, 'assets', 'logo', 'nanhe-mark.svg'), join(here, '..', 'public', 'favicon.svg'));
console.log('Synced brand assets into public/brand');
