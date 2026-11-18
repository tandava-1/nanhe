// Joins the brand's product data (docs/product/products.json, the single source of truth)
// with website-only sample data (prices, ratings, reviews) and the little friends index.
import brand from '../../../docs/product/products.json';
import friends from '../../../assets/characters/characters.json';
import shopData from './shop.json';
import reviewData from './reviews.json';

export type CatKey = 'moisturise' | 'care' | 'hygiene' | 'bath' | 'diapering';

export const CAT_ORDER: CatKey[] = ['moisturise', 'care', 'hygiene', 'bath', 'diapering'];

// Shelf copy from the brand book.
const SHELF: Record<CatKey, { line: string; items: string }> = {
  moisturise: { line: 'Daily softness, from the first massage to bedtime', items: 'Lotion · Massage oil · Rich cream' },
  care: { line: 'For when skin needs fixing or protecting', items: 'Diaper rash cream · Balm · Sunscreen' },
  hygiene: { line: 'The things you reach for ten times a day', items: 'Powder · Bottle wash' },
  bath: { line: 'Bath time, first teeth and grooming, all tear-free and gentle', items: 'Wash · Shampoo · Bubble bath · Toothpaste · Grooming' },
  diapering: { line: 'Diapers and wipes, with a different animal for every size', items: 'Taped diapers · Pants · All wipes' },
};

export const categories = CAT_ORDER.map((key) => ({
  key,
  ...(brand.categories as Record<CatKey, { name: string; base: string; wash: string; deep: string }>)[key],
  ...SHELF[key],
}));

export const catByKey = Object.fromEntries(categories.map((c) => [c.key, c])) as Record<CatKey, (typeof categories)[number]>;

export type Review = {
  stars: number; title: string; body: string; age: string; ageBand: string; skin: string;
  used: string; city?: string; by: string; when: string; helpful: number; reply?: string; free?: boolean;
};

type ShopRow = {
  price: number; rating: number; reviews: number; buyAgain: number; subscribe: boolean;
  routines: string[]; photo?: string; gallery: string[];
};

const shop = shopData as unknown as Record<string, ShopRow>;
const reviewsBySlug = reviewData as unknown as Record<string, { mentions: [string, number][]; reviews: Review[]; questions: { q: string; a: string; by: string; more: number }[] }>;
const friendsBySlug = friends as Record<string, { name: string; animal: string; why: string; file: string }>;

// Unit sale price, shown next to MRP as Legal Metrology expects.
function unitPrice(price: number, size: string): string | null {
  const m = size.match(/^([\d.]+)\s*(ml|g)$/);
  if (m) return `₹${((price / Number(m[1])) * 10).toFixed(1)} per 10 ${m[2]}`;
  const n = size.match(/^(?:(\d+)\s*×\s*)?(\d+)\s*(wipes|diapers|pants)$/);
  if (n) {
    const count = Number(n[1] ?? 1) * Number(n[2]);
    return `₹${(price / count).toFixed(1)} per ${n[3].replace(/s$/, '')}`;
  }
  return null;
}

// Short safety notes for product cards. The full caution text from products.json shows on the product page.
const WARN_SHORT: Record<string, string> = {
  'massage-oil': 'Contains almond oil',
  'mineral-sunscreen': 'For babies 6 months and older',
  'talc-free-powder': "Keep away from baby's face",
  'bubble-bath': 'Not for babies under 12 months',
  'first-toothpaste': 'Fluoride: a rice-grain amount, brushed by an adult',
};

// Age range in months, for the shop's "by age" filter. Diapers go by weight, so these are typical ages.
function ageRange(slug: string, age: string): [number, number] {
  if (slug === 'taped-diapers-nb') return [0, 3];
  if (slug === 'diaper-pants-m') return [6, 24];
  if (/first tooth/i.test(age)) return [6, 36];
  const m = age.match(/(\d+)\s*–\s*(\d+)\s*months/);
  return m ? [Number(m[1]), Number(m[2])] : [0, 36];
}

export const products = brand.products.map((p: any) => {
  const s = shop[p.slug];
  const r = reviewsBySlug[p.slug] ?? { mentions: [], reviews: [], questions: [] };
  return {
    slug: p.slug as string,
    name: (p.name as string[]).join(' '),
    hindi: p.hindi as string,
    category: p.category as CatKey,
    cat: catByKey[p.category as CatKey],
    age: p.age as string,
    line: p.line as string,
    hero: p.hero as string[],
    size: p.size as string,
    natural: p.natural as number | undefined,
    use: p.use as string,
    inci: p.inci as string | undefined,
    contents: p.contents as string | undefined,
    caution: p.caution as string | undefined,
    warnShort: WARN_SHORT[p.slug],
    ageMin: ageRange(p.slug, p.age)[0],
    ageMax: ageRange(p.slug, p.age)[1],
    friend: friendsBySlug[p.slug],
    price: s.price,
    unit: unitPrice(s.price, p.size),
    rating: s.rating,
    reviewCount: s.reviews,
    buyAgain: s.buyAgain,
    subscribe: s.subscribe,
    routines: s.routines,
    photo: s.photo,
    gallery: s.gallery,
    pack: `/brand/packaging/${p.slug}.svg`,
    mentions: r.mentions,
    reviews: r.reviews,
    questions: r.questions,
    isFormula: Boolean(p.inci),
  };
});

export type Product = (typeof products)[number];

export const bySlug = Object.fromEntries(products.map((p) => [p.slug, p])) as Record<string, Product>;

// One entry per character (Susu and Magru each appear on two products).
export const littleFriends = (() => {
  const seen = new Set<string>();
  return products.filter((p) => p.friend && !seen.has(p.friend.name) && seen.add(p.friend.name));
})();

export const ROUTINES = [
  { key: 'bath', label: 'Bath time' },
  { key: 'massage', label: 'Massage' },
  { key: 'nappy', label: 'Nappy change' },
  { key: 'teeth', label: 'First teeth' },
  { key: 'go', label: 'On the go' },
];

export const MADE_WITHOUT = ['Parabens', 'Sulphates (SLS/SLES)', 'Mineral oil', 'Synthetic fragrance', 'Talc', 'Phthalates', 'Artificial dyes'];

export const inr = (n: number) => `₹${n.toLocaleString('en-IN')}`;
