# Publish schedule

Updated Tuesday 25 August 2026 · 5 pages on dates, 1 already live · batch 7 added three new money pages to the queue
Next: nothing. The dates run themselves - each rebuild ships whatever came due.

## Going live this week

**Tuesday 25 August · SEO audit services · Service page · LIVE**
Released on its own date by a rebuild, with nobody deploying by hand. It renders, it is back in `sitemap.xml`, and its inbound links from the services index and the Local SEO hub went live in the same build.

**Tuesday 25 August · SEO packages and pricing · Service page · DUE TODAY**
Re-staged for the batch 7 walkthrough so the release can be watched again. Right now it 404s, it is absent from `sitemap.xml`, and every link pointing at it renders as plain text instead of a dead link. All three flip on the next rebuild after its timestamp.

Two money pages, earliest weekday slots - inside the 2-3 pages a week cap for a domain this age.

## Next up · batch 7

**Thursday 27 August · National SEO services · Service page · SCHEDULED**
Sibling money page under the services branch. 404s until its date, absent from `sitemap.xml`, inbound links render as plain text.

**Tuesday 1 September · Contractor SEO services · Service page · SCHEDULED**
First of the vertical money pages. Same gate applies.

**Thursday 3 September · Roofing SEO · Service page · SCHEDULED**
Second vertical, cross-linked to Contractor SEO. Same gate applies.

Three money pages across two weeks, Tuesdays and Thursdays, never two in a row. That is 2 pages the first week and 2 the next including the packages page, comfortably inside the 10-15 a week ceiling for a domain this age - deliberately slow, because there is no reason to rush a queue nobody is waiting on.

## The launch pages

These five were built before the site went live, so they are the launch, not additions to it. They carry no publish date, which means live on the next deploy - together, the way a launch should look.

Local SEO services · Google Ads management · Local SEO services in Austin · Google Business Profile optimization · SEO vs Google Ads (blog)

## Held pages

None held in this batch. Separately, the three city pages under Local SEO services (Austin, Dallas, Houston) fail the similarity check and need real local material before any fourth city is built. They are already live, so this is a fix-forward job, not a hold.

## How the dates actually work now

Every scheduled page carries a `publishDate`. The build reads it and does three things: the page 404s before its date, it stays out of `sitemap.xml`, and every internal link pointing at it renders as plain text rather than a dead link. On its date, the next rebuild reverses all three at once.

So **any rebuild publishes exactly what came due**. A push does it. The daily GitHub Action does it on the quiet weeks. Nothing here needs flipping by hand, and this file is the human-readable record of the decision, not the mechanism.

Proven Monday 24 August 2026 and again Tuesday 25 August 2026 against the live deploy: the audit page renders and appears twice in `sitemap.xml`, the packages page 404s and appears zero times.

## The daily rebuild Action

Already wired, and it needs nothing from you.

It runs every morning and pushes an empty commit. That is enough: Vercel deploys on every push, and the build releases whatever came due. No deploy hook, no Vercel token, no secrets at all.
