// Standard page, minimally styled to the shipped design system.
// Every quote below is verbatim from context/proof/reviews/reviews-raw.md (pulled 19 August 2026).
// Community wins are labelled as community results - never presented as client work.
const reviewsDescription = "What clients and community members say about working with Your Business, word for word.";

export const metadata = {
  title: "Reviews",
  description: reviewsDescription,
  alternates: { canonical: "/reviews" },
  openGraph: { title: "Reviews | Your Business", description: reviewsDescription, url: "/reviews", type: "website", siteName: "Your Business" },
};

const CLIENT_QUOTES = [
  {
    name: "Troy Angrignon",
    role: "Business Owner",
    quote: "We found Your Business through Jono's YouTube channel. Alex has awesome communication skills, keeps all his commitments, and is super easy to work with. Together we've built content creation, data enrichment, email campaign, website visitor identification, and social listening systems. If you're looking to automate your business I'd strongly recommend reaching out.",
  },
  {
    name: "Nathan Bekmezian",
    role: "Roofing Business Owner, Straightline Design",
    quote: "Before I worked with Jono, my roofing business was running on texts, sticky notes, and way too much manual work. We were dropping the ball on follow-ups, scrambling to keep track of jobs, and honestly, it was a mess. Jono came in and helped me automate almost everything. Lead intake, appointment setting, estimates, contracts, invoices, follow-up — you name it. We used GoHighLevel, PandaDoc, and Make to build out a full system that runs around the clock without me having to babysit it. My reps get booked solid with qualified leads, documents go out automatically, and my production team always has exactly what they need. The cool part is that Jono didn't just automate everything for me, he taught ME how to do it. If you're on the fence about working with Jono, stop hesitating and do it. The amount of time and stress you'll save is insane.",
  },
  {
    name: "Jordan Kilpatrick-Smith",
    role: "Therapy Clinic Owner",
    quote: "Thanks to the systems I've learned and implemented here, my therapy clinic has just signed up its 100th client! Not only changed MY life, but I have 2 full time employees now, with the intention to add 3 more this year. Providing them all with jobs they love, working from home, on their hours with clients they love, and the ability to support their families too while doing it. Your impact ripples through the lives of many.",
  },
  {
    name: "Holly Smith",
    role: "Agency Owner",
    quote: "I know it seems small, but I just automated tasks that have been taking me an hour, two hours to do every single day, sometimes 3 times a day. We've saved over 20 hours of agency work a month just from one automation. (And I'm salivating, we will be completely automated at this rate by end of Q1 2026.) I'm SO encouraged, this group is well worth it.",
  },
];

const COMMUNITY_QUOTES = [
  {
    name: "Mike Partners",
    role: "Community Member",
    quote: "Hey Jono, I am SO thankful I found this community. It's my first day and it's worth thousands from the amount of money I've already saved. If you ever want a video testimonial just let me know. This community should cost significantly more.",
  },
  {
    name: "Julian Bradley",
    role: "Community Member",
    quote: "Let's gooooo!!!!! 75k closed since joining this community!",
  },
];

function Quote({ name, role, quote, tag }: { name: string; role: string; quote: string; tag: string }) {
  return (
    <li style={{ borderTop: "1px solid var(--line-hairline, #e5e4e0)", padding: "28px 0", listStyle: "none" }}>
      <blockquote style={{ margin: 0, color: "var(--text-body, #3f3f3c)" }}>&ldquo;{quote}&rdquo;</blockquote>
      <p style={{ margin: "12px 0 0", color: "var(--text-strong, #1a1a19)", fontWeight: 600 }}>
        {name} <span style={{ color: "var(--text-muted, #73726e)", fontWeight: 400 }}>&middot; {role} &middot; {tag}</span>
      </p>
    </li>
  );
}

export default function Page() {
  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: "96px 24px", fontFamily: "var(--font-core, system-ui)" }}>
      <p style={{ font: "var(--type-label)", letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--text-muted, #73726e)" }}>What clients say</p>
      <h1 style={{ font: "var(--type-h1)", color: "var(--text-strong, #1a1a19)", margin: "10px 0 16px" }}>Reviews</h1>
      <p style={{ color: "var(--text-body, #3f3f3c)" }}>
        Every quote on this page is word for word - nothing paraphrased, nothing written by us.
        60 written testimonials are on record; here are a few. Community results come from members of our free community, not 1-on-1 client work, and are labelled as such.
        The work behind these results is our <a href="/services/local-seo-services" style={{ color: "var(--text-link, #0b62c9)" }}>local SEO services</a>
        and our <a href="/services/google-ads-management" style={{ color: "var(--text-link, #0b62c9)" }}>Google Ads management</a> sprints.
      </p>
      <ul style={{ margin: "40px 0 0", padding: 0 }}>
        {CLIENT_QUOTES.map((q) => <Quote key={q.name} {...q} tag="Client work" />)}
        {COMMUNITY_QUOTES.map((q) => <Quote key={q.name} {...q} tag="Community result" />)}
      </ul>
      <p style={{ marginTop: 40 }}><a href="/contact" style={{ color: "var(--text-link, #0b62c9)" }}>Book a fit call &rarr;</a></p>
      <p style={{ marginTop: 12 }}><a href="/" style={{ color: "var(--text-link, #0b62c9)" }}>&larr; Back to the site</a></p>
    </main>
  );
}
