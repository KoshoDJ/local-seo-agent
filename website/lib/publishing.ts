// The publishing gate. One file decides what is live.
//
// Every scheduled page carries `export const publishDate = "YYYY-MM-DD"`.
// That stamp - not publish-schedule.md - is what actually holds a page back:
// the page 404s before its date, it is filtered out of the sitemap, and every
// inbound link to it renders as plain text until the date passes.
//
// A page with NO date is live. That is correct for everything that was already
// public before the queue existed.

/** Today at midnight UTC, so a page dated today is live all day. */
const startOfToday = () => {
  const now = new Date();
  return new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
};

// A stamp is either a date - "2026-08-27", meaning live from midnight UTC that
// day - or a full timestamp - "2026-08-27T14:30:00Z" - for publishing at an
// exact moment. The date form is what pages normally carry.
export const isLive = (d?: string): boolean => {
  if (!d) return true;
  const exact = d.includes("T");
  const due = new Date(exact ? d : `${d}T00:00:00Z`);
  if (Number.isNaN(due.getTime())) return true; // a broken stamp must never hide a page silently
  return exact ? due <= new Date() : due <= startOfToday();
};

/** Filter any list of dated things down to what has come due. */
export const live = <T extends { publishDate?: string }>(xs: T[]): T[] =>
  xs.filter((x) => isLive(x.publishDate));

// The route registry. Listings, the sitemap and the link helper all read this
// instead of keeping their own hand-maintained copies - a hardcoded list is the
// single most common reason a "scheduled" page shows up early.
//
// Routes absent from this map have no date and are live.
export const SCHEDULE: Record<string, string> = {
  "/services/seo-audit": "2026-08-25T01:42:29Z",
  "/services/seo-packages": "2026-08-25T02:58:00Z",
  "/services/national-seo": "2026-08-25T14:01:41Z",
  "/services/contractor-seo": "2026-09-01T00:00:00Z",
  "/services/roofing-seo": "2026-09-03T00:00:00Z",
};

/** The publish date for a route, or undefined if it has none. */
export const dateFor = (path: string): string | undefined => SCHEDULE[path];

/** Is this route live today? */
export const routeIsLive = (path: string): boolean => isLive(dateFor(path));

/** Every route in a list that is live today. */
export const liveRoutes = (paths: string[]): string[] => paths.filter(routeIsLive);
