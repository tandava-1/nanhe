// The cart lives only in this browser (localStorage). Nothing is sent anywhere.
import { catalog, type Catalog } from './data';

export type CartLine = {
  id: string;
  kind: 'product' | 'kit' | 'box';
  slug: string;            // product slug, kit id, or 'box'
  qty: number;
  subscribe: boolean;
  every?: string;          // subscription frequency
  items?: string[];        // for build-your-own boxes
};

const KEY = 'nanhe-cart';

export function readCart(): CartLine[] {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) ?? '[]') as Partial<CartLine>[];
    return raw.map((l) => ({
      kind: l.kind ?? 'product', subscribe: !!l.subscribe, qty: l.qty ?? 1, slug: l.slug!, every: l.every, items: l.items,
      id: l.id ?? `${l.slug}${l.subscribe ? ':sub' : ''}`,
    }));
  } catch { return []; }
}

export function writeCart(lines: CartLine[]) {
  try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch { /* private mode: cart won't persist */ }
  updateCartBadge();
}

export function addToCart(slug: string, qty = 1, subscribe = false, every?: string) {
  const lines = readCart();
  const id = `${slug}${subscribe ? ':sub' : ''}`;
  const line = lines.find((l) => l.id === id);
  if (line) line.qty += qty; else lines.push({ id, kind: 'product', slug, qty, subscribe, every: subscribe ? every ?? '6 weeks' : undefined });
  writeCart(lines);
}

export function addKit(id: string) {
  const lines = readCart();
  const line = lines.find((l) => l.id === `kit:${id}`);
  if (line) line.qty += 1; else lines.push({ id: `kit:${id}`, kind: 'kit', slug: id, qty: 1, subscribe: false });
  writeCart(lines);
}

export function addBox(items: string[]) {
  const lines = readCart();
  lines.push({ id: `box:${Date.now()}`, kind: 'box', slug: 'box', qty: 1, subscribe: false, items });
  writeCart(lines);
}

export function clearCart() { writeCart([]); }

export function updateCartBadge() {
  const n = readCart().reduce((s, l) => s + l.qty, 0);
  document.querySelectorAll<HTMLElement>('[data-cart-count]').forEach((el) => {
    el.textContent = String(n);
    el.hidden = n === 0;
    el.closest('a')?.setAttribute('aria-label', n ? `Cart, ${n} item${n > 1 ? 's' : ''}` : 'Cart');
  });
}

export const boxOff = (n: number) => (n >= 5 ? 0.15 : n >= 3 ? 0.10 : 0);

/** Price of one unit of a line before subscription discount. */
export function unitPrice(l: CartLine, c: Catalog = catalog()) {
  if (l.kind === 'kit') return c.kits[l.slug]?.price ?? 0;
  if (l.kind === 'box') {
    const sum = (l.items ?? []).reduce((s, x) => s + (c.products[x]?.price ?? 0), 0);
    return Math.round(sum * (1 - boxOff((l.items ?? []).length)));
  }
  return c.products[l.slug]?.price ?? 0;
}

export function totals(lines = readCart(), opts: { cod?: boolean } = {}) {
  const c = catalog();
  let items = 0, subtotal = 0, subSave = 0;
  for (const l of lines) {
    const u = unitPrice(l, c) * l.qty;
    items += l.qty; subtotal += u;
    if (l.subscribe) subSave += Math.round(u * c.rules.subDiscount);
  }
  const code = readCoupon();
  const couponSave = code ? Math.round((subtotal - subSave) * c.rules.coupon.off) : 0;
  const afterDiscounts = subtotal - subSave - couponSave;
  const delivery = items === 0 || afterDiscounts >= c.rules.freeDelivery ? 0 : c.rules.deliveryFee;
  const cod = opts.cod ? c.rules.codFee : 0;
  return { items, subtotal, subSave, couponSave, code, delivery, cod, total: afterDiscounts + delivery + cod, toFree: Math.max(0, c.rules.freeDelivery - afterDiscounts) };
}

export function readCoupon(): string {
  try { return localStorage.getItem('nanhe-coupon') ?? ''; } catch { return ''; }
}
export function writeCoupon(code: string) {
  try { if (code) localStorage.setItem('nanhe-coupon', code); else localStorage.removeItem('nanhe-coupon'); } catch {}
}

export type Gift = { on: boolean; note: string; hidePrices: boolean };
export function readGift(): Gift {
  try { return { on: false, note: '', hidePrices: true, ...JSON.parse(localStorage.getItem('nanhe-gift') ?? '{}') }; } catch { return { on: false, note: '', hidePrices: true }; }
}
export function writeGift(g: Gift) { try { localStorage.setItem('nanhe-gift', JSON.stringify(g)); } catch {} }

export { toast } from './data';
