// Standard page, minimally styled to the shipped design system.
const quoteDescription = "Tell us about your business and get a free graded audit of your search, ads and follow-up by email within minutes.";

export const metadata = {
  title: "Get a quote",
  description: quoteDescription,
  alternates: { canonical: "/quote" },
  openGraph: { title: "Get a quote | Your Business", description: quoteDescription, url: "/quote", type: "website", siteName: "Your Business" },
};

export default function Page() {
  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: "96px 24px", fontFamily: "var(--font-core, system-ui)" }}>
      <p style={{ font: "var(--type-label)", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--text-muted, #73726e)" }}>Start here</p>
      <h1 style={{ font: "var(--type-h1)", color: "var(--text-strong, #1a1a19)", margin: "10px 0 16px" }}>Get a quote</h1>
      <p style={{ color: "var(--text-body, #3f3f3c)" }}>
        Sprint pricing is public: one engine $9,500, both engines $12,500, then a $3,000 a month Growth Retainer if you want us to keep running it - see <a href="/pricing" style={{ color: "var(--text-link, #0b62c9)" }}>pricing</a>.
        The first step is free: fill in the enquiry form and a graded audit of your search, ads and follow-up lands in your inbox within minutes. Then a short fit call, then a 60-minute walkthrough with Jono.
        Not sure which engine you need? Read what the <a href="/services/local-seo-services" style={{ color: "var(--text-link, #0b62c9)" }}>8-week local SEO build</a>
        covers, or how we run <a href="/services/google-ads-management" style={{ color: "var(--text-link, #0b62c9)" }}>Google Ads management</a>, and
        <a href="/blog/seo-vs-google-ads" style={{ color: "var(--text-link, #0b62c9)" }}>SEO vs Google Ads</a> compares the two head to head.
      </p>
      <p style={{ marginTop: 32 }}><a href="/contact" style={{ color: "var(--text-link, #0b62c9)" }}>Go to the enquiry form &rarr;</a></p>
      <p style={{ marginTop: 12 }}><a href="/" style={{ color: "var(--text-link, #0b62c9)" }}>&larr; Back to the site</a></p>
    </main>
  );
}
