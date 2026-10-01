import type { Metadata } from "next";
import "./globals.css";
import { site } from "@/lib/site.config";
import { readFileSync } from "node:fs";
import { join } from "node:path";

// Read at build time and inlined in <head>. Routed through the Tailwind
// pipeline the custom properties resolved to empty at runtime.
const ds = readFileSync(join(process.cwd(), "app", "ds.css"), "utf8");
// Archivo @font-face rules inlined so the stylesheet request stops
// render-blocking. The woff2 files are self-hosted in public/fonts/.
const fontCss = readFileSync(join(process.cwd(), "app", "fonts.css"), "utf8");

// Deliberately a bare shell. The template pages carry their own header, nav and
// footer, so anything added here renders ON TOP of theirs and shows up as a
// stray bar above the promo strip.

export const metadata: Metadata = {
  metadataBase: new URL(site.url),
  title: {
    default: `${site.name} | ${site.city}`,
    template: `%s | ${site.name}`,
  },
  description: site.tagline,
  // Google Cloud Console site verification. Renders
  // <meta name="google-site-verification" content="..." /> into <head>.
  verification: {
    google: "qWh9-LhkNDr1w3xVn_J2hJEcf5ou4YuGS_w0Qmqheas",
  },
};

// Sitewide entity anchor for search and AI engines. The homepage's
// ProfessionalService schema stays page-level; this names the organization
// once, with the profiles AI models resolve the entity against.
const orgSchema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: site.name,
  url: site.url,
  email: site.email,
  sameAs: [
    "https://www.youtube.com/@yourhandle",
    "https://www.linkedin.com/in/yourhandle/",
    "https://instagram.com/jono_catliff",
    "https://tiktok.com/@yourhandle",
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(orgSchema) }}
        />
        {/* Archivo is what --font-core asks for. Without it every heading falls
            back to Helvetica and the display sizes stop reading as display. */}
        <link
          rel="preload"
          href="/fonts/archivo-latin.woff2"
          as="font"
          type="font/woff2"
          crossOrigin=""
        />
        <style dangerouslySetInnerHTML={{ __html: ds }} />
        <style dangerouslySetInnerHTML={{ __html: fontCss }} />
      </head>
      <body>{children}</body>
    </html>
  );
}
