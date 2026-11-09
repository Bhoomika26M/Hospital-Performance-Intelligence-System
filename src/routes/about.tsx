import { createFileRoute } from "@tanstack/react-router";
import { Database, Target, Users, Wrench } from "lucide-react";

import { PageHeader } from "@/components/page-header";

export const Route = createFileRoute("/about")({
  head: () => ({
    meta: [
      { title: "About the Project — MedTrack_DV" },
      {
        name: "description",
        content: "Objectives, scope, tools and team of the MedTrack_DV healthcare analytics project.",
      },
      { property: "og:title", content: "About the Project — MedTrack_DV" },
      {
        property: "og:description",
        content: "Objectives, scope, tools and team of the MedTrack_DV healthcare analytics project.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: AboutPage,
});

const objectives = [
  "Turn raw healthcare data into clear, interactive visual dashboards.",
  "Give a single place to explore hospital operations, patient movement, clinical patterns and resource use.",
  "Apply the full data science workflow — collection, cleaning, analysis and visualisation — to a real-world domain.",
  "Support data-informed discussion about hospital performance and planning.",
];

const tools = [
  { name: "Tableau Public", role: "Dashboard design and publishing" },
  { name: "[Data preparation tool]", role: "e.g. Python / Excel — to be confirmed" },
  { name: "MedTrack_DV website", role: "Presentation layer for the dashboards" },
];

const team = [
  { label: "Student", value: "Evelin Shaju" },
  { label: "Department", value: "Data Science" },
];

function AboutPage() {
  return (
    <div className="space-y-10">
      <PageHeader
        eyebrow="About Project"
        title="About MedTrack_DV"
        description="MedTrack_DV is a healthcare analytics project that presents its findings through four interactive Tableau Public dashboards. The goal is to make hospital data easier to understand by organising it into focused, visual stories."
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="rounded-2xl border bg-card p-6 shadow-card lg:col-span-2">
          <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground">
            <Target className="size-5 text-primary" /> Objectives
          </h2>
          <ul className="mt-4 space-y-3">
            {objectives.map((o, i) => (
              <li key={o} className="flex gap-3 text-sm leading-relaxed text-muted-foreground">
                <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-accent text-xs font-semibold text-accent-foreground">
                  {i + 1}
                </span>
                {o}
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-2xl border bg-card p-6 shadow-card">
          <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground">
            <Users className="size-5 text-primary" /> Project team
          </h2>
          <dl className="mt-4 space-y-3 text-sm">
            {team.map((t) => (
              <div key={t.label} className="flex justify-between gap-3 border-b pb-2 last:border-0">
                <dt className="text-muted-foreground">{t.label}</dt>
                <dd className="text-right font-medium text-foreground">{t.value}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <section className="rounded-2xl border bg-card p-6 shadow-card">
          <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground">
            <Wrench className="size-5 text-primary" /> Tools & data
          </h2>
          <ul className="mt-4 divide-y">
            {tools.map((t) => (
              <li key={t.name} className="flex items-center justify-between gap-3 py-3 text-sm">
                <span className="font-medium text-foreground">{t.name}</span>
                <span className="text-right text-muted-foreground">{t.role}</span>
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-2xl border bg-gradient-soft p-6">
          <h2 className="flex items-center gap-2 text-xl font-semibold text-foreground">
            <Database className="size-5 text-primary" /> Scope
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
            The project covers four analytical areas — Hospital Overview, Patient Flow, Clinical
            Analytics and Resource Utilization. All figures shown come directly from the
            published Tableau dashboards; this website does not add or calculate any statistics
            of its own.
          </p>
        </section>
      </div>
    </div>
  );
}
