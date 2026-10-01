import type { MetadataRoute } from "next";
import { site } from "@/lib/site.config";
import { liveRoutes } from "@/lib/publishing";

export const dynamic = "force-static"; // required for static export (SSG)

// The sitemap mirrors your page tree exactly.
// DELIBERATELY EXCLUDED: /thank-you (must never be indexed - it would
// wreck your conversion count) and the legal pages (no search value).
export default function sitemap(): MetadataRoute.Sitemap {
  const pages = [
    "", "/services", "/about", "/contact", "/quote", "/reviews", "/pricing",
    "/services/seo-audit",
    "/services/seo-packages",
    "/services/national-seo",
    "/services/contractor-seo",
    "/services/roofing-seo",
    "/services/local-seo-services",
    "/services/local-seo-services/austin",
    "/services/local-seo-services/dallas",
    "/services/local-seo-services/houston",
    "/services/google-ads-management",
    "/services/google-business-profile-optimization",
    "/blog",
    "/blog/seo-vs-google-ads",
    "/blog/how-to-do-a-local-seo-audit",
    "/blog/seo-for-contractors",
    "/blog/google-business-profile-audit",
  ];
  // Future-dated pages leave the sitemap until their publishDate.
  return liveRoutes(pages).map((path) => ({
    url: `${site.url}${path}`,
    lastModified: new Date(),
    priority: path === "" ? 1 : 0.8,
  }));
}
