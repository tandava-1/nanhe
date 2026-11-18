// The baby profile lives only in this browser. Nothing is sent anywhere.
// It also writes the short `nanhe-baby` record ({ageBand, skin}) that product pages read for "babies like yours".
export type Baby = {
  name: string;
  born: boolean;          // false = expecting
  month: string;          // YYYY-MM: month of birth, or the due month when expecting
  skin: string;           // normal | dry | sensitive | eczema | unsure
  concerns: string[];
  climate: string;        // humid | dry | cold
};
export type Profile = { babies: Baby[]; active: number };

const KEY = 'nanhe-profile';

export function readProfile(): Profile | null {
  try {
    const p = JSON.parse(localStorage.getItem(KEY) ?? 'null');
    return p && Array.isArray(p.babies) && p.babies.length ? p : null;
  } catch { return null; }
}

export function writeProfile(p: Profile | null) {
  try {
    if (!p || !p.babies.length) { localStorage.removeItem(KEY); localStorage.removeItem('nanhe-baby'); return; }
    localStorage.setItem(KEY, JSON.stringify(p));
    const b = p.babies[p.active] ?? p.babies[0];
    const band = ageBand(ageMonths(b));
    localStorage.setItem('nanhe-baby', JSON.stringify({ ageBand: band, skin: b.skin === 'unsure' ? '' : b.skin }));
  } catch { /* private mode: the profile just won't persist */ }
}

export function activeBaby(): Baby | null {
  const p = readProfile();
  return p ? p.babies[p.active] ?? p.babies[0] : null;
}

/** Whole months since birth; negative while expecting; null if no date. */
export function ageMonths(b: Baby): number | null {
  if (!b.month) return null;
  const [y, m] = b.month.split('-').map(Number);
  const now = new Date();
  return (now.getFullYear() - y) * 12 + (now.getMonth() + 1 - m);
}

export function ageBand(months: number | null): string {
  if (months === null) return '';
  if (months < 3) return '0-3';
  if (months < 6) return '3-6';
  if (months < 12) return '6-12';
  return '12-36';
}

export function describeAge(b: Baby): string {
  const m = ageMonths(b);
  if (m === null) return '';
  if (!b.born || m < 0) return m < 0 ? `due in ${-m} month${m === -1 ? '' : 's'}` : 'due this month';
  if (m < 1) return 'newborn';
  if (m < 24) return `${m} month${m === 1 ? '' : 's'}`;
  return `${Math.floor(m / 12)} years`;
}

export const SKIN_LABEL: Record<string, string> = { normal: 'Normal', dry: 'Dry', sensitive: 'Sensitive', eczema: 'Eczema-prone', unsure: 'Not sure' };
