import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, BookOpen, FlaskConical } from "lucide-react";

import heroImage from "@/assets/hero-medtrack.jpg";
import { Button } from "@/components/ui/button";
import { DASHBOARDS, toTableauEmbedUrl } from "@/lib/dashboards";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "MedTrack_DV — Healthcare Analytics Dashboards" },
      {
        name: "description",
        content:
          "MedTrack_DV brings four Tableau Public healthcare dashboards together: hospital overview, patient flow, clinical analytics and resource utilization.",
      },
      { property: "og:title", content: "MedTrack_DV — Healthcare Analytics Dashboards" },
      {
        property: "og:description",
        content:
          "Four Tableau Public healthcare dashboards: hospital overview, patient flow, clinical analytics and resource utilization.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <div className="space-y-12">
      <section className="relative overflow-hidden rounded-3xl bg-sidebar shadow-elegant">
        <img
          src={heroImage}
          alt=""
          width={1600}
          height={800}
          className="absolute inset-0 h-full w-full object-cover opacity-90"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-sidebar via-sidebar/80 to-transparent" />
        <div className="relative max-w-2xl px-6 py-14 md:px-12 md:py-20 animate-fade-up">
          <h1 className="text-4xl font-semibold text-sidebar-foreground md:text-5xl">
            MedTrack_DV
          </h1>
          <p className="mt-4 text-lg leading-relaxed text-sidebar-muted">
            A healthcare analytics showcase that brings four interactive Tableau Public dashboards
            together in one place — from hospital-wide overview to resource utilization.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button asChild size="lg" variant="secondary">
              <Link to="/hospital-overview">
                Explore dashboards <ArrowRight />
              </Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="ghost"
              className="text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground"
            >
              <Link to="/about">About the project</Link>
            </Button>
          </div>
        </div>
      </section>

      <section>
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.18em] text-primary">
              Dashboards
            </p>
            <h2 className="mt-2 text-2xl font-semibold text-foreground md:text-3xl">
              Four views of hospital performance
            </h2>
          </div>
        </div>

        <div className="mt-6 grid gap-5 sm:grid-cols-2">
          {DASHBOARDS.map((d) => {
            const linked = toTableauEmbedUrl(d.tableauUrl) !== null;
            return (
              <Link
                key={d.path}
                to={d.path}
                className="group relative flex flex-col rounded-2xl border bg-card p-6 shadow-card transition hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-elegant"
              >
                <div className="flex items-start justify-between">
                  <span className="flex size-12 items-center justify-center rounded-xl bg-gradient-primary text-primary-foreground">
                    <d.icon className="size-6" />
                  </span>
                  <span className="font-display text-3xl font-semibold text-primary-soft transition group-hover:text-accent">
                    {d.number}
                  </span>
                </div>
                <h3 className="mt-5 text-xl font-semibold text-foreground">{d.title}</h3>
                <p className="mt-2 flex-1 text-sm leading-relaxed text-muted-foreground">
                  {d.summary}
                </p>
                <div className="mt-5 flex items-center justify-between text-sm">
                  <span className="flex items-center gap-2 text-muted-foreground">
                    <span
                      className={
                        linked ? "size-2 rounded-full bg-success" : "size-2 rounded-full bg-warning"
                      }
                    />
                    {linked ? "Dashboard linked" : "Link pending"}
                  </span>
                  <span className="flex items-center gap-1 font-medium text-primary">
                    Open <ArrowRight className="size-4 transition group-hover:translate-x-0.5" />
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <Link
          to="/about"
          className="group flex items-start gap-4 rounded-2xl border bg-gradient-soft p-6 transition hover:border-primary/40"
        >
          <BookOpen className="mt-1 size-6 shrink-0 text-primary" />
          <div>
            <h3 className="text-lg font-semibold text-foreground">About the project</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Objectives, scope, tools and the team behind MedTrack_DV.
            </p>
          </div>
        </Link>
        <Link
          to="/methodology"
          className="group flex items-start gap-4 rounded-2xl border bg-gradient-soft p-6 transition hover:border-primary/40"
        >
          <FlaskConical className="mt-1 size-6 shrink-0 text-primary" />
          <div>
            <h3 className="text-lg font-semibold text-foreground">Methodology & limitations</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              How the data was prepared and visualised, and what to keep in mind.
            </p>
          </div>
        </Link>
      </section>
    </div>
  );
}
