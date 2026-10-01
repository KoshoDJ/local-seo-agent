"use client";

import { useSearchParams } from "next/navigation";
import { useState } from "react";

// The star filter. 4-5 goes straight to Google; 1-3 becomes a save-the-customer
// alert instead of a public one-star.
//
// The site is a STATIC EXPORT (output: "export" in next.config.mjs), so there
// are no API routes to hide a webhook behind - a server route would 404 on the
// deploy and every complaint would vanish. So the form POSTs Make.com directly,
// which its gateway allows (access-control-allow-origin: *) and which lets us
// read the real response instead of guessing that it sent.
//
// The trade-off, stated plainly: the webhook URL is visible in the page source.
// It is write-only - the worst anyone can do with it is post junk into the
// scenario - and this is the standard shape for a static site. If that ever
// matters, drop output: "export" and move the POST behind a server route.

type Props = { googleReviewUrl: string | null; feedbackWebhook: string | null };

// A URL parameter is untrusted input - anyone holding the link can edit it.
// React renders {value} as text so there is no injection, but a 4,000-character
// "name" would still wreck the layout, so everything gets capped.
const cap = (value: string | null, limit: number) => (value ?? "").trim().slice(0, limit);

const STARS = [1, 2, 3, 4, 5] as const;

export default function ReviewForm({ googleReviewUrl, feedbackWebhook }: Props) {
  const params = useSearchParams();

  const name = cap(params.get("name"), 60);
  const email = cap(params.get("email"), 200);
  const cid = cap(params.get("cid"), 120);
  const firstName = name.split(" ")[0] ?? "";
  // Known contact = the ask was sent to them, so we already have their details
  // and must not ask again. Prefilled means invisible, not editable.
  const known = Boolean(cid || email || name);

  const [rating, setRating] = useState<number | null>(null);
  const [hovered, setHovered] = useState<number | null>(null);
  const [feedback, setFeedback] = useState("");
  const [walkupName, setWalkupName] = useState("");
  const [walkupContact, setWalkupContact] = useState("");
  const [state, setState] = useState<"idle" | "sending" | "sent" | "error">("idle");
  const [error, setError] = useState("");

  // Picking a star ONLY selects it. Nothing sends and nothing navigates here -
  // an instant redirect on tap meant the fields below were never filled in and
  // the happy path was never captured at all. Everything happens on submit.
  function pick(value: number) {
    setRating(value);
    setState("idle");
    setError("");
  }

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (rating === null) return;
    const happy = rating >= 4;
    // Happy path still needs somewhere to send them once the record is saved.
    if (happy && !googleReviewUrl) {
      setState("error");
      setError("The Google review link is not connected yet, so this button has nowhere to send you.");
      return;
    }
    // No webhook and a happy rating: still send them to Google rather than
    // blocking a 5-star review over a missing config value.
    if (!feedbackWebhook) {
      if (happy) {
        window.location.href = googleReviewUrl as string;
        return;
      }
      setState("error");
      setError("The feedback destination is not connected yet, so this would not reach anyone.");
      return;
    }
    setState("sending");
    setError("");
    try {
      const res = await fetch(feedbackWebhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          rating,
          feedback: feedback.trim().slice(0, 5000),
          name: (known ? name : walkupName).trim().slice(0, 120),
          email,
          contact: known ? "" : walkupContact.trim().slice(0, 120),
          cid,
          // "link" = sent to a known contact, details come from the CRM.
          // "qr" = walk-up scan, details are self-reported. The GHL workflow
          // tags these differently.
          source: known ? "link" : "qr",
          page: typeof window === "undefined" ? "" : window.location.href,
        }),
      });
      if (!res.ok) throw new Error(`The message did not send (error ${res.status}).`);
      // Every rating is recorded first, THEN the happy path goes to Google.
      // Google has NO prefill parameter for the review body (their policy: a
      // review must be the reviewer's own words), so the closest legitimate
      // help is putting what they already wrote on their clipboard to paste.
      if (happy) {
        const words = feedback.trim();
        if (words) {
          try {
            await navigator.clipboard.writeText(words);
          } catch {
            // Clipboard blocked (permissions, http, older browser). Never let
            // this stop the redirect - the review matters more than the paste.
          }
        }
        window.location.href = googleReviewUrl as string;
        return;
      }
      setState("sent");
    } catch (caught) {
      setState("error");
      setError(caught instanceof Error ? caught.message : "That did not send.");
    }
  }

  const card: React.CSSProperties = {
    background: "var(--surface-card)",
    borderTop: "3px solid var(--surface-accent)",
    borderRadius: "var(--radius-card)",
    padding: "var(--pad-card-lg)",
    display: "grid",
    gap: "var(--space-6)",
  };
  const field: React.CSSProperties = {
    width: "100%",
    padding: "var(--pad-control)",
    font: "var(--type-body)",
    lineHeight: "var(--lh-body)",
    color: "var(--text-strong)",
    background: "var(--surface-sunken)",
    border: "var(--border-hairline) solid var(--line-hairline)",
    borderRadius: "var(--radius-input)",
    outline: "none",
  };
  const label: React.CSSProperties = {
    font: "var(--type-label)",
    letterSpacing: "var(--track-label)",
    textTransform: "uppercase",
    color: "var(--text-muted)",
  };

  if (state === "sent") {
    return (
      <div style={card}>
        <h1 style={{ font: "var(--type-heading)", letterSpacing: "var(--track-heading)", color: "var(--text-strong)", margin: 0 }}>
          Thank you - that went straight to the owner.
        </h1>
        <p style={{ font: "var(--type-body-lg)", color: "var(--text-body)", margin: 0, maxWidth: "50ch" }}>
          Not a form that disappears into an inbox. Someone reads this personally, usually within the hour, and you
          will hear back from a person about fixing it.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={submit} style={card}>
      <div style={{ display: "grid", gap: "var(--space-2)", justifyItems: "center", textAlign: "center" }}>
        <span className="gw-label">{firstName ? `Hi ${firstName} · 30 seconds` : "30 seconds"}</span>
        <h1 style={{ margin: 0, maxWidth: "26ch" }}>
          How was your experience with us?
        </h1>
        <p style={{ font: "var(--type-body-lg)", color: "var(--text-body)", margin: 0, maxWidth: "42ch" }}>
          One tap. If something went wrong we would rather hear it here than read it later.
        </p>
      </div>

      <div role="radiogroup" aria-label="Your rating" style={{ display: "flex", gap: "var(--space-3)", flexWrap: "wrap", justifyContent: "center" }}>
        {STARS.map((value) => {
          const lit = value <= (hovered ?? rating ?? 0);
          return (
            <button
              key={value}
              type="button"
              role="radio"
              aria-checked={rating === value}
              aria-label={`${value} star${value === 1 ? "" : "s"}`}
              onClick={() => pick(value)}
              onMouseEnter={() => setHovered(value)}
              onMouseLeave={() => setHovered(null)}
              onFocus={() => setHovered(value)}
              onBlur={() => setHovered(null)}
              style={{
                width: "84px",
                height: "84px",
                display: "grid",
                placeItems: "center",
                cursor: "pointer",
                background: lit ? "var(--surface-accent-soft)" : "var(--surface-sunken)",
                border: `var(--border-hairline) solid ${lit ? "var(--surface-accent)" : "var(--line-hairline)"}`,
                borderRadius: "var(--radius-pill)",
                transition: "var(--transition-control)",
              }}
            >
              <svg viewBox="0 0 24 24" width="42" height="42" aria-hidden="true"
                fill={lit ? "var(--surface-accent)" : "none"}
                stroke={lit ? "var(--surface-accent)" : "var(--text-muted)"}
                strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
                <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.12 2.12 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.12 2.12 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.12 2.12 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.12 2.12 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.166-.755a2.12 2.12 0 0 0 1.597-1.16z" />
              </svg>
            </button>
          );
        })}
      </div>

      {rating !== null && (
        <div style={{ display: "grid", gap: "var(--space-5)" }}>
          <label style={{ display: "grid", gap: "6px" }}>
            <span style={label}>{rating >= 4 ? "What stood out?" : "What went wrong?"}</span>
            <textarea
              required={rating < 4}
              rows={5}
              value={feedback}
              onChange={(event) => setFeedback(event.target.value)}
              placeholder={rating >= 4
                ? "A sentence or two on what we did well. We'll copy it to your clipboard so you can paste it straight into Google."
                : "Tell us what happened. The more specific, the faster we can fix it."}
              style={{ ...field, resize: "vertical" }}
            />
          </label>

          {/* Walk-up path only. Someone scanning a QR code arrives with nothing
              in the URL, and they are still worth catching. Both fields optional. */}
          {!known && (
            <div style={{ display: "grid", gap: "var(--space-5)" }}>
              <p style={{ font: "var(--type-body-sm)", color: "var(--text-muted)", margin: 0 }}>
                {rating >= 4 ? "Who should we thank? Both optional." : "So we can actually fix this, who should we call? Both optional - the message sends either way."}
              </p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-5)" }}>
                <label style={{ display: "grid", gap: "6px" }}>
                  <span style={label}>Your name</span>
                  <input value={walkupName} onChange={(e) => setWalkupName(e.target.value)} placeholder="Your name" style={field} />
                </label>
                <label style={{ display: "grid", gap: "6px" }}>
                  <span style={label}>Phone or email</span>
                  <input value={walkupContact} onChange={(e) => setWalkupContact(e.target.value)} placeholder="How to reach you" style={field} />
                </label>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={state === "sending"}
            style={{
              display: "inline-flex", alignItems: "center", justifyContent: "center", gap: "8px",
              fontSize: "var(--size-body)", borderRadius: "var(--radius-pill)",
              border: "var(--border-hairline) solid var(--accent-900)",
              cursor: state === "sending" ? "wait" : "pointer",
              minHeight: "var(--control-h-lg)", padding: "var(--pad-control-lg)",
              background: "var(--surface-accent)", color: "var(--text-on-accent)",
              width: "100%", opacity: state === "sending" ? 0.7 : 1,
            }}
          >
            {state === "sending" ? "Sending..." : rating >= 4 ? "Continue to Google" : "Send this to the owner"}
          </button>
          <span style={{ font: "var(--type-caption)", color: "var(--text-muted)" }}>
            {rating >= 4
              ? "We'll copy your words to the clipboard and open Google - paste and post."
              : "This goes to the owner directly. It is not posted anywhere public."}
          </span>
        </div>
      )}

      {state === "error" && (
        <p role="alert" style={{ font: "var(--type-body-sm)", color: "var(--status-critical)", margin: 0 }}>
          {error} Please call {" "}
          <a href="tel:+15550000000" style={{ color: "var(--status-critical)" }}>(555) 000-0000</a> and we will sort it out.
        </p>
      )}
    </form>
  );
}
