---
name: discount-codes
description: Finds working discount codes, coupons, and stackable savings for any online store, from a screenshot of the cart or checkout page or just a store URL. Runs deep web research across coupon aggregators, Reddit, forums, the brand's own promos, and cashback portals, then hands back a ranked try-in-this-order list with expected savings. Use when the user screenshots a checkout page, pastes a store link, or says "find me a discount code", "any coupons for this", "am I overpaying", "check for promo codes", or "/discount-codes". Do not use for B2B SaaS contract negotiation, for travel fare hunting (flights and hotels need a different method), or for anything requiring the user's payment details.
---

# Discount Codes

Turns a screenshot of any cart or checkout page into a ranked list of discount codes to try, in order, with an honest estimate of what each one saves. The job is not to dump every code that ever existed for the store. It is to hand back the three to five moves most likely to actually work right now, plus the savings levers that need no code at all.

## When to use / when not to use

**Use when** the user is mid-checkout and wants to know if they are leaving money on the table. A screenshot of the cart, the checkout page, or a product page is the ideal input. A bare store URL works too.

**Do not use for** flights or hotels, B2B software contract negotiation, anything that requires entering the user's payment or login details, or grey-market codes (employee-only, reseller, stolen accounts).

## Inputs

One of:
1. A **screenshot** of the cart, checkout, or product page. Preferred, because it carries the cart total, the items, the currency, and the promo field.
2. A **store URL** or store name.

Optionally: the user's country, whether they are a new customer, and whether they qualify for student, military, healthcare, or birthday pricing.

If given a screenshot, read it first and state back what was found before researching. If the store is ambiguous, ask once, do not guess.

## Process

### 1. Read the page

From the screenshot or URL, extract and state back:

- Store domain and brand name
- Currency and country storefront (a .co.uk cart takes different codes than a .com cart)
- Cart subtotal and item count
- The specific items, with product names or SKUs where visible
- Whether a promo or discount field exists, and whether one is already applied
- Free shipping threshold, if it is displayed
- Whether the user appears logged in or is checking out as a guest

If any of that is not visible, say so rather than assuming it.

### 2. Research, in this order

Run the searches in parallel where possible. Do not stop at the first aggregator, they are the least reliable source.

**Tier 1, highest hit rate:**
- The brand's own site: a promotions, offers, deals, or sale page, plus the footer. Brands publish their own live codes more often than people expect.
- Expect a 403 on many DTC storefronts. Shopify and Cloudflare block automated fetches, so a failed fetch is not evidence there is no promo. When the site blocks, fall back to searching `<brand> newsletter signup discount`, `<brand> first order discount`, and `<brand> current sale`, and say the site could not be read directly.
- The brand's newsletter or SMS signup offer. The first-order code is usually the single biggest discount available (commonly 10 to 20 percent) and it is always real.
- The brand's current sitewide sale, since many sitewide sales block additional codes and that changes the whole recommendation.

**Tier 2, community sourced and usually current:**
- Reddit: search in plain language, `reddit <brand> promo code what worked` and `reddit <brand> discount code`. Do NOT use the `site:reddit.com` operator, it returns eBay and Wikipedia noise instead of threads. Weight toward the last 6 months. Check the brand's own subreddit and any deal subreddits.
- Slickdeals, DealNews, and forum threads for the brand.
- Creator and affiliate codes: search `<brand> code` plus YouTube, Instagram, and podcast sponsorship phrasing. Sponsor codes are almost always live and stack least often but discount most reliably.

**Tier 3, aggregators, verify before trusting:**
- RetailMeNot, CouponFollow, Honey, Coupons.com, Wethrift, Dealspotr, Knoji.
- Treat every aggregator code as unverified. They keep expired codes live for the traffic. Use them for candidate generation only, and downgrade confidence accordingly.

**Tier 4, no-code savings levers, always check these:**
- Student, military, healthcare, teacher, first responder verification programs (SheerID, ID.me, Student Beans, UNiDAYS).
- Birthday and loyalty program discounts.
- Cashback portals and cards (Rakuten, TopCashback, Honey Gold, card-linked offers). These stack with codes almost every time.
- Cart abandonment: leaving the cart for 24 to 48 hours with an email on file triggers a recovery code at a large share of DTC brands. This is often the single highest-value play and costs nothing but a day.
- Free shipping threshold: if the cart sits just under it, name the gap and the cheapest add-on to clear it.
- Refurbished, open box, or last-season variants of the exact item.
- Price history and price matching, where the retailer honors it.

### 3. Filter and score

Kill any candidate that is:
- Region locked to a storefront the user is not on
- Expired, where a date is visible
- Conditional on a minimum spend the cart does not meet, unless the gap is small enough to be worth naming
- First-order only, when the user is a returning customer
- Grey market: employee codes, reseller codes, codes tied to someone else's account

Score every survivor on two axes: **confidence** (how likely it works, based on source tier and recency) and **savings** (dollar or percent value on this specific cart).

### 4. Order the attempts

Rank by expected value, meaning confidence multiplied by savings, not by headline percentage. A 40 percent code from an aggregator with no recency signal is worth less than a verified 15 percent newsletter code.

Also state whether codes stack at this store, if that is discoverable, and if they do, name the correct stack order.

## Output format

Deliver in chat, in this shape. No file gets written unless asked.

```
STORE: <brand> (<domain>, <currency> storefront)
CART: <subtotal>, <n> items <, free shipping at $X, currently $Y short>

TRY IN THIS ORDER
1. <CODE> — <what it does> — saves ~<$ or %> — confidence: high/medium/low — source: <where it came from>
2. <CODE> — ...
3. <CODE> — ...

NO CODE NEEDED
- <lever>: <what to do, and what it is worth>
- <lever>: <what to do, and what it is worth>

STACK: <do codes stack here, and in what order, or "one code only">
BEST CASE: <total savings if everything lands> on a <subtotal> cart
NOTE: <anything that would change the answer, such as an active sitewide sale that blocks codes>
```

Keep it to five codes maximum. If nothing credible turns up, say that plainly and lead with the no-code levers instead. An honest "there are no live codes, but the newsletter popup gives you 15 percent and Rakuten adds 4 percent back" is a better answer than five dead codes.

## Example

Input: a screenshot of a Vuori cart, $184 subtotal, two items, US storefront, guest checkout.

```
STORE: Vuori (vuori.com, USD storefront)
CART: $184.00, 2 items, free shipping already met at $75

TRY IN THIS ORDER
1. WELCOME20 — first order, 20 percent off — saves ~$36.80 — confidence: high — source: brand newsletter popup, verified on site
2. <CREATOR>20 — podcast sponsor code, 20 percent off first order — saves ~$36.80 — confidence: high — source: active sponsorship read, last 60 days
3. FRIENDS15 — 15 percent sitewide — saves ~$27.60 — confidence: low — source: aggregator, no recency signal

NO CODE NEEDED
- Cart abandonment: add the email at checkout, walk away 48 hours. Vuori sends recovery offers. Worth 10 to 20 percent on top of nothing.
- Rakuten: 3 to 8 percent cash back, stacks with a code. On $184 that is $6 to $15 back.
- Final sale section: the same styles in last season colorways run 40 to 50 percent off.

STACK: one code only, cash back stacks on top of it
BEST CASE: about $52 off a $184 cart, roughly 28 percent
NOTE: first-order codes will not fire if this email has ordered before. Use a fresh email or expect the sitewide code instead.
```

## Hard rules / Never do

- **Never invent a code.** Every code output must trace to a real source found in this run. If a source cannot be named, the code does not ship. A fabricated code costs the user trust and thirty seconds at checkout for nothing.
- **Never overstate confidence.** Aggregator codes are low confidence by default, always. Say so.
- **Never enter anything on the user's behalf.** No signups, no email submissions, no checkout, no payment details. Research and report only. The user does the typing.
- **Never recommend grey-market codes.** No employee discounts, no reseller codes, no account sharing, no codes obtained by misrepresenting eligibility. Student and military codes get listed only with the verification requirement stated plainly.
- **Never bury the no-code levers.** They are often worth more than the codes and they almost always work. Cart abandonment and cashback in particular.
- **Never pad the list.** Five codes maximum. Three good ones beat fifteen dead ones.
- **State the date sensitivity.** Codes rot. Note that the answer reflects what is live today.
- **Never treat a blocked page as an answer.** A 403 means unknown, not none. Say which sources could not be read.
