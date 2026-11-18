// The cart lives only in this browser (localStorage). Nothing is sent anywhere.
export type CartLine = { slug: string; qty: number; subscribe: boolean };

const KEY = 'nanhe-cart';

export function readCart(): CartLine[] {
  try { return JSON.parse(localStorage.getItem(KEY) ?? '[]'); } catch { return []; }
}

function writeCart(lines: CartLine[]) {
  try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch { /* private mode: cart just won't persist */ }
}

export function addToCart(slug: string, qty = 1, subscribe = false) {
  const lines = readCart();
  const line = lines.find((l) => l.slug === slug && l.subscribe === subscribe);
  if (line) line.qty += qty; else lines.push({ slug, qty, subscribe });
  writeCart(lines);
  updateCartBadge();
}

export function updateCartBadge() {
  const n = readCart().reduce((s, l) => s + l.qty, 0);
  document.querySelectorAll<HTMLElement>('[data-cart-count]').forEach((el) => {
    el.textContent = String(n);
    el.hidden = n === 0;
    el.closest('a')?.setAttribute('aria-label', n ? `Cart, ${n} item${n > 1 ? 's' : ''}` : 'Cart');
  });
}

let timer: number | undefined;
export function toast(msg: string) {
  const el = document.querySelector<HTMLElement>('[data-toast]');
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
  window.clearTimeout(timer);
  timer = window.setTimeout(() => el.classList.remove('show'), 3200);
}
