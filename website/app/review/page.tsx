import { Suspense } from "react";
import { site } from "@/lib/site.config";
import ReviewForm from "./review-form";

// The review filter (/review-generator). Deliberately noindex: this is a page
// customers are sent to by link or QR, never something Google should rank, and
// an indexed review-gate page is a bad look in the SERP.
//
// Minimal chrome on purpose - no nav, no footer links. Every exit on this
// screen is a review that does not get written.

export const metadata = {
  title: "Leave a review",
  description: "Tell Aperture Studio how we did.",
  robots: { index: false, follow: false },
  alternates: { canonical: "/review" },
};

export default function Page() {
  return (
    <div className="sc-host" data-sc-name="Local Service Site Template">
      <div style={{ background: "var(--surface-tint)", color: "var(--text-body)", minHeight: "100vh", display: "grid", gridTemplateRows: "auto 1fr" }}>
        <header style={{ background: "var(--surface-card)", borderBottom: "var(--border-hairline) solid var(--line-hairline)" }}>
          <div className="gw-container" style={{ display: "flex", alignItems: "center", height: "74px" }}>
            <a href="/" style={{ display: "grid", gap: "2px", textDecoration: "none" }}>
              <span style={{ font: "var(--weight-black) 21px/1 var(--font-core)", letterSpacing: "-0.03em", color: "var(--text-strong)" }}>Aperture Studio</span>
              <span style={{ font: "var(--type-label)", letterSpacing: "var(--track-label)", textTransform: "uppercase", color: "var(--text-muted)" }}>Weddings &amp; Portraits</span>
            </a>
          </div>
        </header>

        <main className="gw-container" style={{ padding: "var(--space-9) var(--gutter)", display: "grid", justifyContent: "center", alignContent: "center" }}>
          <div style={{ width: "min(100%, 620px)" }}>
            <Suspense fallback={<div style={{ minHeight: "420px" }} />}>
              <ReviewForm googleReviewUrl={site.googleReviewUrl} feedbackWebhook={site.reviewFeedbackWebhook} />
            </Suspense>
          </div>
        </main>
      </div>
    </div>
  );
}
