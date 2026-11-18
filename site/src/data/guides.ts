// Parent guides. SAMPLE COPY: general, widely given baby-care guidance, written plainly. Every guide must be
// reviewed and signed off by the brand's paediatrician before launch; until then pages say so.
export type Guide = {
  slug: string; title: string; minutes: number; topic: string; stages: string[]; image: string; imageAlt: string; imagePos?: string;
  summary: string; takeaways: string[]; need: string[]; steps: { title: string; body: string }[];
  parentTips: { quote: string; by: string }[]; doctor: string[]; related: string[];
};

export const TOPICS = [
  { key: 'bathing', label: 'Bathing' }, { key: 'massage', label: 'Massage & oils' }, { key: 'nappy', label: 'Nappy rash' },
  { key: 'dry', label: 'Dry skin & eczema' }, { key: 'teeth', label: 'First teeth' }, { key: 'hair', label: 'Hair & cradle cap' },
];
export const STAGES = [
  { key: 'expecting', label: 'Expecting' }, { key: '0-3', label: '0–3 months' }, { key: '3-6', label: '3–6 months' },
  { key: '6-12', label: '6–12 months' }, { key: '12-36', label: '1–3 years' },
];

export const GUIDES: Guide[] = [
  {
    slug: 'first-bath', title: "Baby's first bath, step by step", minutes: 4, topic: 'bathing', stages: ['expecting', '0-3'],
    image: '/brand/renders/ai-04-bath-shelf.jpg', imageAlt: "Lotion and powder on a bathroom shelf beside a towel and a baby's foot",
    summary: 'What you need, how warm the water should be, and how to keep it short and calm.',
    takeaways: ['Sponge baths until the umbilical cord stump falls off.', 'Warm, not hot: test the water with your elbow or the inside of your wrist.', 'Five to ten minutes is plenty, and a few baths a week is enough in the early months.', 'Never leave your baby alone in water, not even for a second.'],
    need: ['head-to-toe-wash', 'daily-lotion', 'water-wipes'],
    steps: [
      { title: 'Get everything ready first', body: 'Towel, a soft cloth, a clean nappy, fresh clothes and a little mild wash, all within reach. Warm the room. Once your baby is in the water, both your hands stay with them.' },
      { title: 'Check the water', body: 'A few centimetres of water is enough. It should feel comfortably warm on your elbow, never hot. Swirl it so there are no hot spots.' },
      { title: 'Face first, with plain water', body: 'Wipe the eyes from the inner corner outwards with a fresh part of the cloth each time. The face needs only water.' },
      { title: 'Body, then the folds', body: 'Use a small amount of mild wash. Clean the neck, armpits, behind the ears and the nappy area last. Support the head and neck the whole time.' },
      { title: 'Pat dry and moisturise', body: "Lift your baby straight into the towel and pat, don't rub, paying attention to the folds. Smooth on a fragrance-free moisturiser within a few minutes, while the skin is still a little damp." },
    ],
    parentTips: [{ quote: 'Warm the towel on the geyser pipe first. She cried far less.', by: 'Parent of a 2-month-old' }, { quote: 'Bath right before the last feed. Best sleep of the day.', by: 'Parent of a 3-month-old' }],
    doctor: ['The skin around the cord stump is red, swollen, smells, or oozes', 'Your baby has a fever, or a rash with a fever', 'Your baby seems unusually floppy, drowsy or won’t feed'],
    related: ['daily-maalish', 'hair-washing'],
  },
  {
    slug: 'daily-maalish', title: 'The daily maalish: how-to, and which oils to use', minutes: 6, topic: 'massage', stages: ['0-3', '3-6', '6-12'],
    image: '/brand/renders/ai-02-maalish.jpg', imageAlt: "Hands massaging a baby's back with oil, a bottle of golden oil beside them",
    summary: 'A calm routine many Indian families already love, done gently and with the right oil.',
    takeaways: ['Pick a time when your baby is awake and content, not straight after a feed.', 'Warm a little oil in your palms; you need less than you think.', 'Use long, gentle strokes and stop if your baby gets fussy.', 'Patch test a new oil, and skip nut oils if there’s a nut allergy in the family.'],
    need: ['massage-oil', 'water-wipes'],
    steps: [
      { title: 'Set up somewhere warm', body: 'A warm room, a soft towel on a flat surface, and a little oil in a bowl. Keep your nails short and take off rings.' },
      { title: 'Legs and feet', body: 'Warm a few drops between your palms. Stroke from thigh to ankle, then gently rub the soles with your thumbs.' },
      { title: 'Tummy and chest', body: 'Make slow clockwise circles on the tummy, then stroke outwards across the chest from the middle, like opening a book.' },
      { title: 'Arms and hands', body: 'Stroke from shoulder to wrist and gently open the fingers. Babies often like this part best.' },
      { title: 'Back, then rest', body: 'With your baby on their tummy, stroke from neck to bottom. Keep oil away from the face and eyes, then cuddle or bathe.' },
    ],
    parentTips: [{ quote: 'Nani does the legs, I do the back. He falls asleep halfway.', by: 'Parent of a 3-month-old' }],
    doctor: ['A rash or redness appears where the oil was used', 'Your baby cries in pain when you touch a particular spot', 'Swelling, wheezing or hives after using a nut oil'],
    related: ['first-bath', 'dry-skin'],
  },
  {
    slug: 'nappy-rash', title: 'Nappy rash: what helps, and when to see a doctor', minutes: 5, topic: 'nappy', stages: ['0-3', '3-6', '6-12', '12-36'],
    imagePos: 'center 22%', image: '/brand/renders/ai-07-rash-cream-labelled.jpg', imageAlt: 'A cream tube standing on its sage cap between calendula flowers',
    summary: 'Most nappy rash settles in a few days with frequent changes, air and a barrier cream.',
    takeaways: ['Change wet or dirty nappies promptly, including at night if the rash is bad.', 'Clean gently with water or water wipes, then let the skin dry fully.', 'A thin layer of zinc barrier cream at every change protects the skin.', 'Some nappy-free time each day helps more than anything else.'],
    need: ['diaper-rash-cream', 'water-wipes', 'taped-diapers-nb'],
    steps: [
      { title: 'Change often', body: 'Wetness and contact with stool are the main causes. Check and change more often while the skin is red.' },
      { title: 'Clean gently', body: 'Use water or a water wipe and pat, don’t rub. Avoid scented wipes and soaps on sore skin.' },
      { title: 'Let it breathe', body: 'Leave the nappy off on a towel for a few minutes after each change, or longer when you can.' },
      { title: 'Protect with a barrier', body: 'Once the skin is dry, apply a thin layer of zinc oxide cream. You don’t need to scrub it all off at the next change.' },
      { title: 'Check the fit', body: 'A nappy that is too tight rubs. Size up if you see red marks at the waist or legs.' },
    ],
    parentTips: [{ quote: 'Nappy-free time on a towel after the morning bath fixed it faster than any cream.', by: 'Parent of a 5-month-old' }],
    doctor: ['Blisters, pus, open sores or oozing', 'A fever, or your baby seems unwell', 'Bright red rash with small red spots around the edges, or spreading beyond the nappy area', 'No better after two or three days of good care'],
    related: ['dry-skin', 'first-bath'],
  },
  {
    slug: 'hair-washing', title: 'Hair washing without tears, and cradle cap', minutes: 3, topic: 'hair', stages: ['0-3', '3-6', '6-12', '12-36'],
    image: '/brand/renders/ai-10-bath-shampoo.jpg', imageAlt: "An adult rinses a baby's foamy hair with water from a brass lota",
    summary: 'How to keep water out of the eyes, and what to do about the scaly patches called cradle cap.',
    takeaways: ['Tilt the head back and pour water from the forehead backwards.', 'A coin-sized amount of mild shampoo is enough.', 'Cradle cap is common and harmless; soften it with a little oil, then brush gently.', 'Don’t pick at the scales.'],
    need: ['tear-free-shampoo', 'head-to-toe-wash', 'massage-oil'],
    steps: [
      { title: 'Support and tilt', body: 'Hold your baby along your forearm with the head slightly back. Older babies can lean back against you.' },
      { title: 'Shield the eyes', body: 'Cup your hand across the forehead like a visor, or pour from a lota behind the hairline.' },
      { title: 'Lather lightly', body: 'Massage a coin-sized amount of shampoo into wet hair with your fingertips, then rinse well.' },
      { title: 'For cradle cap', body: 'Rub a little oil into the scales and leave it for a while before the bath. Brush gently with a soft brush, then wash it out.' },
    ],
    parentTips: [{ quote: 'The lota from behind the head works better than any cup.', by: 'Parent of an 18-month-old' }],
    doctor: ['Cradle cap that spreads to the face or body, or looks red and inflamed', 'Patches that are weeping, crusted or bleeding', 'Your baby seems itchy or uncomfortable'],
    related: ['first-bath', 'daily-maalish'],
  },
  {
    slug: 'first-teeth', title: 'First teeth: when to start brushing, and how much toothpaste', minutes: 3, topic: 'teeth', stages: ['3-6', '6-12', '12-36'],
    image: '/brand/packaging/first-toothpaste.svg', imageAlt: 'First Toothpaste tube with Magru the crocodile cub',
    summary: 'Start before the first tooth, then brush twice a day with a rice-grain smear of fluoride toothpaste.',
    takeaways: ['Before teeth: wipe the gums with a soft cloth or finger brush once a day.', 'From the first tooth: brush twice a day with fluoride toothpaste.', 'Under 3, use a smear the size of a grain of rice, and an adult does the brushing.', 'No need to rinse afterwards; just wipe away the excess.'],
    need: ['finger-toothbrush', 'first-toothpaste'],
    steps: [
      { title: 'Before the first tooth', body: 'Once a day, gently rub the gums with a clean, damp cloth or a silicone finger brush. It gets your baby used to it.' },
      { title: 'From the first tooth', body: 'Brush morning and night. Use a smear of fluoride toothpaste no bigger than a grain of rice.' },
      { title: 'How to brush', body: 'Sit your baby on your lap facing away, cup the chin, and brush in small, gentle circles along the gum line.' },
      { title: 'After brushing', body: 'Wipe away the extra toothpaste. Rinsing washes the fluoride away, so skip it.' },
    ],
    parentTips: [{ quote: 'We brush in front of the mirror and she copies me.', by: 'Parent of a 14-month-old' }],
    doctor: ['White chalky spots or brown marks on the teeth (see a dentist)', 'Swollen, bleeding gums', 'Your child swallows a large amount of toothpaste'],
    related: ['hair-washing', 'nappy-rash'],
  },
  {
    slug: 'dry-skin', title: 'Dry skin and eczema-prone skin', minutes: 5, topic: 'dry', stages: ['0-3', '3-6', '6-12', '12-36'],
    image: '/brand/renders/ai-05-ingredients.jpg', imageAlt: 'Coconut, oats, calendula, neem, almonds, shea butter and ghee on a pale surface',
    summary: 'Short baths, fragrance-free products and moisturising within minutes of the bath do most of the work.',
    takeaways: ['Keep baths short and lukewarm.', 'Choose fragrance-free products.', 'Moisturise within a few minutes of the bath, and again whenever skin feels dry.', 'Soft cotton clothes, and watch dry air from AC or heaters.'],
    need: ['rich-cream', 'daily-lotion', 'all-purpose-balm'],
    steps: [
      { title: 'Short, lukewarm baths', body: 'Hot water and long baths strip the skin. Five to ten minutes in lukewarm water is plenty.' },
      { title: 'Pat dry, then moisturise straight away', body: 'Pat the skin dry and apply a moisturiser within a few minutes, while it is still a little damp. Use a richer cream on dry patches.' },
      { title: 'Moisturise often', body: 'Two or three times a day on dry areas helps more than one thick layer. Cheeks, elbows and knees dry out first.' },
      { title: 'Mind the air and clothes', body: 'AC and room heaters dry the air. Dress your baby in soft cotton and avoid scratchy wool against the skin.' },
    ],
    parentTips: [{ quote: 'Cream straight after the bath, before the vest goes on. That habit changed everything.', by: 'Parent of a 7-month-old' }],
    doctor: ['Skin that is cracked, weeping, crusting or bleeding', 'Patches that look infected: yellow crust, pus or spreading redness', 'Itching that disturbs your baby’s sleep', 'No improvement after a couple of weeks of good care'],
    related: ['first-bath', 'daily-maalish'],
  },
];

export const QUICK = [
  { q: 'How often should I bathe my newborn?', a: 'A few times a week is enough in the early months, with sponge baths until the cord stump falls off. Wipe the face, neck folds and nappy area every day.', guide: 'first-bath' },
  { q: 'Is mustard oil safe for baby massage?', a: 'Many paediatricians now suggest avoiding mustard oil on young babies’ skin, because it can irritate and dry the skin barrier. Lighter oils such as coconut are a gentler choice. Patch test any oil first.', guide: 'daily-maalish' },
  { q: 'Can I use adult sunscreen on my baby?', a: 'For babies under 6 months, shade and light clothing are better than any sunscreen. From 6 months, a mineral (zinc oxide) sunscreen made for babies is the gentler choice.', guide: null },
  { q: 'What does “tear-free” actually mean?', a: 'It means the product is formulated to be mild on the eyes. It can still sting a little, so keep it away from the eyes and rinse with water if any gets in.', guide: 'hair-washing' },
  { q: 'Should I use baby powder?', a: 'Many parents don’t need it. If you do, choose a talc-free powder, shake it into your palm away from your baby’s face, and pat it onto skin folds. Never shake it over your baby.', guide: null },
  { q: 'When should I start brushing?', a: 'As soon as the first tooth appears, twice a day with a rice-grain smear of fluoride toothpaste. Before that, wipe the gums once a day.', guide: 'first-teeth' },
];

export const DOCTOR_ALWAYS = ['A rash with a fever', 'Blisters, pus, oozing or crusted skin', 'A rash that spreads quickly', 'Your baby seems unwell, very drowsy, or won’t feed'];

export const guideBySlug = Object.fromEntries(GUIDES.map((g) => [g.slug, g]));
