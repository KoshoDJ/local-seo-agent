---
description: Google Business Profile setup - full research, every field generated, paste-ready in 30 minutes
argument-hint: [focus: categories | services | description | hours | photos | attributes | service-area | products | citations | faq]
---

**Focus mode:** if a subpoint is named (`/gbp-build citations`, `/gbp-build services`), run ONLY that section of the spec at full depth - e.g. `/gbp-build citations` runs just the citation campaign from `references/citations.md`, `/gbp-build services` just the 30-50 service extraction with keyword volumes. No focus = the full setup below.

Set up (or overhaul) my Google Business Profile. **Read `references/gbp-setup.md` and execute it end to end - it IS the spec.** Follow its steps exactly; this command only adds the repo wiring:

**Repo wiring (before Step 1):**
- Read `context/business.md`, `context/proof/proof-inventory.md`, and `context/voice.md` first - skip every question those files already answer. The proof inventory feeds the description, services, and attributes (identity items like family-owned only if TRUE there).
- **Ask the country FIRST, before any volume lookup.** Semrush keeps a separate keyword database per country and **defaults to the US**. Pull US data for a business in Manchester, Calgary or Auckland and every volume on the profile is for the wrong country - the service list looks researched and is quietly worthless. Ask "which country are your customers searching from?", take it from `context/business.md` if the service area is already recorded there, set the database to match (`us`, `uk`, `ca`, `au`, `nz`, `ie`...), **say on screen which database you're using**, and record it in CLAUDE.md "## My setup" so it's never asked twice.

- **Rank services by `[service] [city]` volume, but NEVER put the city in the service name.** Semrush cannot geo-target below country level, so appending the city is the only way to isolate real local demand - that is why the query has it. The city is a measuring device, not part of the answer.
  - Query: `emergency plumber toronto` → 2,400/mo. **Service name on the profile: "Emergency Plumber".** Never "Emergency Plumber Toronto".
  - Google already knows where the business is - that's what the profile IS. Stuffing the city into service names is the single most common GBP keyword-stuffing pattern and it is a suspension risk, not a ranking one.
  - Between close variants, the city-appended query picks the winner: "couples therapy toronto" 1,300/mo beats "couples counselling toronto" 590/mo, so the service is named **"Couples Therapy"**.
  - Target **70 services - 50 to use plus 20 EXTRAS - ranked by that volume, highest first** - the profile has room and the high-volume ones must not be buried below whatever the website happened to list.
  - Keyword volumes: Semrush where available; autocomplete + judgment otherwise, marked as estimates.
- The citation section (spec section 12): pull the tiers from `references/citations.md` - Tier 1 + 2 hardcoded from there, Tier 3 aggregators noted, Tier 4 industry-specific researched live per that file's rule.

**The spec's own flow (hold me to it):**
1. **Inputs** - the required/recommended/nice-to-have questions, one batch at a time
2b. **Anti-stuffing pass, before anything is finalized** - run the spec's "stuffing rules" over categories AND services: every entry must be something the business actually delivers, one entry per bookable job (merge duplicate phrasings and report what was merged), no city and no keyword strings in any name. Extras are presented as OPTIONS, never as slots to fill. Predefined services get swept exhaustively first, then custom ones with descriptions.

2. **Deep research (always oversupply - see the spec's OVERSUPPLY RULE)** - 20 categories (10 + 10 extras), 70 services (50 + 20 extras), 30 products (20 + 10 extras). People reject some of everything, and an unfilled slot is wasted ranking surface. Every extra carries a one-line "use this if". Then: website fetch, top-3 competitor teardown (their categories, services, reviews), LIVE category verification (never invent - verify via the reference URLs + competitors' actual primaries), nearby cities for SAB, **50 services ranked by `[service] [city]` search volume and named WITHOUT the city**, products, attributes discovery, keyword gap
3. **The research summary checkpoint** - show me the summary block and WAIT for my confirm before generating
4. **Generate `gbp-{business-slug}.md`** - all 12 sections, every rule applied. Categories, services and products each render as TWO blocks: "USE THESE" then "EXTRAS" with the swap-in reason on each. (9 secondary categories filled, description first-100-chars rule, 24/7 only if real, identity attributes, service area ≤20 cities / ≤2h drive)
5. **Suspension-proofing** - run the full checklist; any flag = warn me BEFORE finalizing. **The business name always gets an explicit verdict, clean or not** (per the spec's "name verdict" section) - a clean name is stated as clean, with the keyword-stuffed version of MY name and MY city spelled out in full as the thing never to change it to. Never let the name pass silently: it is rarely stuffed at setup and often stuffed months later by someone acting on bad advice, and it is the one field where a ranking tactic costs the whole profile.
6. **Handoff** - the paste-into-GBP walkthrough, photos brief, and the citation campaign as the follow-up (per `references/citations.md`: Tier 1+2 manually, aggregators for the long tail, industry directories by hand, quarterly NAP re-check)

Output stays legible: the final file is copy-paste sections in plain English, YAML only where the spec requires it.

---

## The second deliverable: `gbp-{business-slug}.html` - the dashboard you fill the profile from

**Every run also writes one self-contained HTML page and opens it.** The markdown file is the record; the HTML is the thing you actually work from - one screen, open beside the Google Business Profile editor, copying field by field. It is also the version that reads on a screen recording, which the markdown never does.

**⛔ The markdown is the single source of truth. Generate the HTML from it, never the other way round.** Regenerate the WHOLE file every time the markdown changes - never hand-edit it, never patch it incrementally. Stale HTML that disagrees with the file is worse than no HTML.

**Copy the house style from `keyword-map.html` verbatim** - same CSS block, same tokens: cream canvas `#f5f4ed`, ivory cards `#faf9f5` at 16px radius with a hairline border and soft shadow, sand `#eeece3` for header rows, coral `#d97757` for the small uppercase mono labels, JetBrains Mono for anything that gets copied, system sans for everything else. One file, self-contained, inline CSS, no external scripts or images. It opens in any browser with no server.

**Every field is one click to copy. This is the point of the whole deliverable.**

Each copyable value sits in its own card with a **Copy** button, and a tiny inline `<script>` does `navigator.clipboard.writeText()` and flips the button to "Copied" for a second. No framework, about fifteen lines. A field the owner has to select by hand, in a long scrolling page, next to a form with a character limit, is exactly where the mistakes happen.

**What the dashboard holds, in this order:**

1. **The header** - business name, the primary category, the city, the date, and the Semrush database the volumes came from. **The name gets its suspension verdict right here**, stated in words: clean, or flagged with the exact stuffed version never to paste in.
2. **Categories** - primary first and marked as such, then the nine secondaries, then the EXTRAS block with each one's "use this if" line. Each name copyable on its own, because they go into Google one at a time.
3. **Services** - the 50, ranked by volume, highest first, each with its monthly search number in mono on the right. Then the 20 extras below a divider. **The city never appears in a service name** - if one does, the anti-stuffing pass failed and the dashboard must not launder it.
4. **The description** - in a single card with a live character count against the 750 limit, and the first 100 characters visibly marked, because that is the part that shows before the fold.
5. **Products** - the 20 plus 10 extras, each with its name, price and description copyable together.
6. **Hours, attributes and the service area** - attributes split into confirmed and "only if true", since identity attributes are the ones that get claimed carelessly.
7. **Photos brief** - what to shoot and how many, as a checklist.
8. **Citations** - the master record pinned at the top with each field copyable, because the whole point is that it is identical everywhere. **Then every directory listed by name, in its tier, each as a real checkbox with its URL as a link** - Tier 1, Tier 2, the aggregators, and the industry sites. A ticked row strikes through and fades, so the page doubles as the worksheet for the seven hours it takes. **⛔ Never write a count instead of the list.** "33 directories" with nothing under it is the one section of this dashboard that is useless on its own: the whole job is working down the names, and a number sends the owner back to the markdown file to find them.

**Rules, same as every other deliverable here:** plain English in every string, no jargon, real values only - never a placeholder that looks like data. No em-dashes. Volumes marked as estimates where they are estimates, rather than presented as measured. One dashboard per business: re-running overwrites it, and the markdown keeps the history.

**End the chat report with the clickable absolute path on its own line** - `file:///.../gbp-{business-slug}.html` - so it opens in one click.
