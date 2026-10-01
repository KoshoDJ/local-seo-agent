// THE SERVICES MANIFEST - the single source of truth for the /services index.
//
// ⛔ /scale-map and /service-page add ONE ENTRY HERE when they build a service
// page. They never edit app/services/page.tsx, which renders this list.
//
// Why this file exists: the index used to be hand-written JSX, so a new page's
// link got appended next to whichever link happened to be last. Four unrelated
// services ended up filed under the "SEO Audit Services" heading. Data cannot
// make that mistake - every entry renders as its own section, in this order.
//
// Nested city pages belong in `children`, not as top-level entries.

export type ServiceEntry = {
  slug: string;          // route under /services/
  title: string;         // the H2 on the index
  blurb: string;         // one or two sentences, plain text
  image: string;         // /images/... public path
  alt: string;
  children?: { slug: string; label: string }[];  // city pages nested under it
};

export const services: ServiceEntry[] = [
  // /service-page adds one entry here per page it writes.
];
