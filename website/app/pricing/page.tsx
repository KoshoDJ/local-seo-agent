import { ScheduledLink } from "@/components/ScheduledLink";
// Standard page, minimally styled to the shipped design system.
// Prices come from context/business.md (verified 19 August 2026). Fees in USD.
const pricingDescription = "Sprint pricing: one engine $9,500, both engines $12,500, Growth Retainer $3,000 a month. All fees in USD.";

export const metadata = {
  title: "Pricing",
  description: pricingDescription,
  alternates: { canonical: "/pricing" },
  openGraph: { title: "Pricing | Your Business", description: pricingDescription, url: "/pricing", type: "website", siteName: "Your Business" },
};

const OFFERS = [
  {
    name: "SEO Sprint or Google Ads Sprint",
    price: "$9,500",
    detail: "One growth engine, built end to end in eight weeks. $9,500 paid in full within 7 days of your call, or $11,500 in 3 installments.",
  },
  {
    name: "Full Sprint",
    price: "$12,500",
    detail: "Both engines - SEO and Google Ads - in the same eight weeks. $12,500 paid in full, or $15,000 in 3 installments.",
  },
  {
    name: "Growth Retainer",
    price: "$3,000/mo",
    detail: "After the sprint: we run the ads and SEO, host the platform and keep optimizing. Month to month, no lock-in.",
  },
  {
    name: "Out-of-sprint projects",
    price: "$3,000",
    detail: "Anything outside the sprint scope, priced per project.",
  },
];

export default function Page() {
  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: "96px 24px", fontFamily: "var(--font-core, system-ui)" }}>
      <p style={{ font: "var(--type-label)", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--text-muted, #73726e)" }}>What it costs</p>
      <h1 style={{ font: "var(--type-h1)", color: "var(--text-strong, #1a1a19)", margin: "10px 0 16px" }}>Pricing</h1>
      <p style={{ color: "var(--text-body, #3f3f3c)" }}>
        Every sprint includes the foundation: CRM, speed-to-lead, sales automations, website fixes and tracking.
        Payment is 50% to kick off and 50% at the midpoint, once the core systems are live in your account. All fees in USD.
        The two engines these prices buy are our <a href="/services/local-seo-services" style={{ color: "var(--text-link, #0b62c9)" }}>local SEO services</a>
        and our <a href="/services/google-ads-management" style={{ color: "var(--text-link, #0b62c9)" }}>Google Ads management</a>, with
        <a href="/services/google-business-profile-optimization" style={{ color: "var(--text-link, #0b62c9)" }}>Business Profile optimization</a> built into the SEO side.
      </p>
      <ul style={{ listStyle: "none", margin: "40px 0 0", padding: 0 }}>
        {OFFERS.map((o) => (
          <li key={o.name} style={{ borderTop: "1px solid var(--line-hairline, #e5e4e0)", padding: "24px 0" }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "baseline" }}>
              <strong style={{ color: "var(--text-strong, #1a1a19)", font: "var(--type-h3)" }}>{o.name}</strong>
              <strong style={{ color: "var(--text-strong, #1a1a19)", whiteSpace: "nowrap" }}>{o.price}</strong>
            </div>
            <p style={{ color: "var(--text-body, #3f3f3c)", margin: "8px 0 0" }}>{o.detail}</p>
          </li>
        ))}
      </ul>
      <p style={{ marginTop: 32, color: "var(--text-body, #3f3f3c)" }}>
        The guarantee: live in 8 weeks or we keep working free. Our 1-on-1 services are reserved for businesses doing $25K+ a month.
      </p>
      <p style={{ marginTop: 24, color: "var(--text-body, #3f3f3c)" }}>
        Want the SEO side of this laid out in full - what each package covers, and what happens after the eight weeks?
        That lives on <ScheduledLink href="/services/seo-packages" style={{ color: "var(--text-link, #0b62c9)" }}>SEO packages and pricing</ScheduledLink>.
      </p>
      <p style={{ marginTop: 32 }}><a href="/contact" style={{ color: "var(--text-link, #0b62c9)" }}>Book a fit call &rarr;</a></p>
      <p style={{ marginTop: 12 }}><a href="/" style={{ color: "var(--text-link, #0b62c9)" }}>&larr; Back to the site</a></p>
    </main>
  );
}
