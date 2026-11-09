import { useEffect, useRef, useState } from "react";
import {
  AlertTriangle,
  BarChart3,
  ExternalLink,
  Link2,
  Loader2,
  Maximize2,
  RotateCw,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { toTableauEmbedUrl } from "@/lib/dashboards";

interface TableauEmbedProps {
  title: string;
  url: string;
}

type LoadState = "loading" | "loaded" | "error";

/** How long to wait for Tableau Public before showing the error message. */
const LOAD_TIMEOUT_MS = 30000;

export function TableauEmbed({ title, url }: TableauEmbedProps) {
  const frameRef = useRef<HTMLDivElement>(null);
  const embedUrl = toTableauEmbedUrl(url);
  const [mounted, setMounted] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [status, setStatus] = useState<LoadState>("loading");

  // Create the iframe only after hydration so its load event is never missed.
  useEffect(() => setMounted(true), []);

  useEffect(() => {
    if (!embedUrl || !mounted) return;
    setStatus("loading");
    if (typeof navigator !== "undefined" && !navigator.onLine) {
      setStatus("error");
      return;
    }
    const timer = window.setTimeout(() => {
      setStatus((s) => (s === "loading" ? "error" : s));
    }, LOAD_TIMEOUT_MS);
    const onOffline = () => setStatus((s) => (s === "loading" ? "error" : s));
    window.addEventListener("offline", onOffline);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener("offline", onOffline);
    };
  }, [embedUrl, mounted, attempt]);

  const goFullscreen = () => {
    frameRef.current?.requestFullscreen?.();
  };

  const retry = () => setAttempt((a) => a + 1);

  const statusDot = !embedUrl
    ? "size-2 rounded-full bg-warning animate-pulse"
    : status === "error"
      ? "size-2 rounded-full bg-destructive"
      : status === "loading"
        ? "size-2 rounded-full bg-warning animate-pulse"
        : "size-2 rounded-full bg-success";

  const statusText = !embedUrl
    ? "Awaiting Tableau Public link"
    : status === "error"
      ? "Dashboard could not load"
      : status === "loading"
        ? "Loading from Tableau Public…"
        : "Live from Tableau Public";

  return (
    <section className="overflow-hidden rounded-2xl border bg-card shadow-card">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b px-5 py-3">
        <div className="flex items-center gap-2 text-sm">
          <span className={statusDot} />
          <span className="font-medium text-foreground">{statusText}</span>
        </div>
        {embedUrl && (
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={goFullscreen}>
              <Maximize2 /> Full screen
            </Button>
            <Button variant="default" size="sm" asChild>
              <a href={url} target="_blank" rel="noreferrer">
                <ExternalLink /> Open in Tableau
              </a>
            </Button>
          </div>
        )}
      </div>

      <div ref={frameRef} className="relative bg-card">
        {embedUrl ? (
          <>
            {mounted && status !== "error" && (
              <iframe
                key={`${embedUrl}-${attempt}`}
                title={`${title} — Tableau dashboard`}
                src={embedUrl}
                onLoad={() => setStatus("loaded")}
                className="block h-[calc(100vh-8rem)] min-h-[520px] w-full border-0 md:min-h-[640px]"
                allowFullScreen
              />
            )}

            {(!mounted || status === "loading") && (
              <div
                role="status"
                className="absolute inset-0 flex min-h-[520px] items-center justify-center bg-gradient-soft px-6"
              >
                <div className="absolute inset-0 bg-grid opacity-60" aria-hidden />
                <div className="relative text-center">
                  <Loader2 className="mx-auto size-10 animate-spin text-primary" />
                  <p className="mt-4 font-medium text-foreground">Loading {title} dashboard…</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    Connecting to Tableau Public. This can take a few seconds.
                  </p>
                </div>
              </div>
            )}

            {status === "error" && (
              <div
                role="alert"
                className="relative flex h-[calc(100vh-8rem)] min-h-[520px] items-center justify-center bg-gradient-soft px-6 md:min-h-[640px]"
              >
                <div className="absolute inset-0 bg-grid opacity-60" aria-hidden />
                <div className="relative max-w-md text-center">
                  <div className="mx-auto flex size-16 items-center justify-center rounded-2xl bg-card text-destructive shadow-card">
                    <AlertTriangle className="size-8" />
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-foreground">
                    The {title} dashboard couldn't load
                  </h3>
                  <p className="mt-2 text-sm text-muted-foreground">
                    Tableau Public didn't respond. Check your internet connection and try again,
                    or open the dashboard directly on Tableau Public.
                  </p>
                  <div className="mt-6 flex flex-wrap justify-center gap-2">
                    <Button onClick={retry}>
                      <RotateCw /> Try again
                    </Button>
                    <Button variant="outline" asChild>
                      <a href={url} target="_blank" rel="noreferrer">
                        <ExternalLink /> Open in Tableau
                      </a>
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="relative flex h-[70vh] min-h-[480px] items-center justify-center bg-gradient-soft px-6">
            <div className="absolute inset-0 bg-grid opacity-60" aria-hidden />
            <div className="relative max-w-md text-center">
              <div className="mx-auto flex size-16 items-center justify-center rounded-2xl bg-gradient-primary text-primary-foreground shadow-elegant">
                <BarChart3 className="size-8" />
              </div>
              <h3 className="mt-6 text-xl font-semibold text-foreground">
                {title} dashboard goes here
              </h3>
              <p className="mt-2 text-sm text-muted-foreground">
                This space is reserved for the interactive Tableau Public dashboard. It will
                appear here once the dashboard link is added.
              </p>
              <div className="mt-5 inline-flex items-center gap-2 rounded-full border bg-card px-4 py-1.5 text-xs text-muted-foreground">
                <Link2 className="size-3.5" />
                public.tableau.com/views/…
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
