// THE BLOG MANIFEST - the single source of truth for the /blog index.
//
// ⛔ /blog-post and /scale-map add ONE ENTRY HERE when they write a post.
// They never edit app/blog/page.tsx, which renders this list.
//
// The index filters on publish date, so a scheduled post does not appear at
// all until it is live. The old hardcoded index had no gate whatsoever - it
// would have linked straight to a 404 the first time a post carried a date.

export type PostEntry = {
  slug: string;
  kicker: string;   // "Contractors · 24 August 2026"
  title: string;
  blurb: string;
};

export const posts: PostEntry[] = [
  // /blog-post adds one entry here per post it writes.
];
