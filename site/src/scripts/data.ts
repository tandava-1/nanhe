// Reads the catalog JSON that <CatalogData /> puts in the page, and small helpers shared by page scripts.
export type CP = {
  slug: string; name: string; hindi: string; category: string; catName: string; price: number; size: string;
  unit: string | null; pack: string; rating: number; reviewCount: number; buyAgain: number; age: string;
  ageMin: number; ageMax: number; subscribe: boolean; mentions: [string, number][]; hero: string[];
  warnShort: string | null; friend: string | null;
};
export type Kit = { id: string; name: string; items: string[]; price: number; sum: number; cat: string };
export type Catalog = {
  rules: { freeDelivery: number; deliveryFee: number; codFee: number; subDiscount: number; coupon: { code: string; off: number } };
  products: Record<string, CP>;
  kits: Record<string, Kit>;
};

let cached: Catalog | null = null;
export function catalog(): Catalog {
  if (!cached) cached = JSON.parse(document.getElementById('catalog-data')!.textContent!);
  return cached!;
}

export const inr = (n: number) => `₹${Math.round(n).toLocaleString('en-IN')}`;

export function esc(s: string) {
  return s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]!));
}

export function toast(msg: string) {
  const el = document.querySelector<HTMLElement>('[data-toast]');
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
  window.clearTimeout((el as any)._t);
  (el as any)._t = window.setTimeout(() => el.classList.remove('show'), 3400);
}

// Sample "babies like yours" figure: derived from the sample rating and fixed share tables, so it is stable.
const AGE_SHARE: Record<string, number> = { '0-3': .24, '3-6': .3, '6-12': .28, '12-36': .18 };
const SKIN_SHARE: Record<string, number> = { normal: .4, dry: .18, sensitive: .3, eczema: .12 };
function hash(s: string) { let h = 7; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 997; return h; }
export function likeYours(slug: string, rating: number, count: number, ageBand = '', skin = '') {
  const share = (ageBand ? AGE_SHARE[ageBand] ?? 1 : 1) * (skin ? SKIN_SHARE[skin] ?? 1 : 1);
  const n = Math.max(3, Math.round(count * share));
  const off = ((hash(slug + ageBand + skin) % 5) - 1) / 10;
  return { rating: Math.min(5, Math.max(3.8, rating + off)), n };
}

export const AGE_TXT: Record<string, string> = { '0-3': '0–3 months', '3-6': '3–6 months', '6-12': '6–12 months', '12-36': '1–3 years' };
export const SKIN_TXT: Record<string, string> = { normal: 'normal skin', dry: 'dry skin', sensitive: 'sensitive skin', eczema: 'eczema-prone skin' };
