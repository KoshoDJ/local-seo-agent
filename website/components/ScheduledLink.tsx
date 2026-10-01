// A link that knows whether its target has been published yet.
//
// Before the target's publishDate it renders as plain text, so a scheduled page
// never gets a live inbound link pointing at a 404. On its date the same build
// that publishes the page turns every one of these into a real link - no skill
// run, no manual pass, no orphan.
import { routeIsLive } from "@/lib/publishing";
import type { CSSProperties, ReactNode } from "react";

export function ScheduledLink({
  href,
  style,
  children,
}: {
  href: string;
  style?: CSSProperties;
  children: ReactNode;
}) {
  if (!routeIsLive(href)) return <span style={style}>{children}</span>;
  return (
    <a href={href} style={style}>
      {children}
    </a>
  );
}
