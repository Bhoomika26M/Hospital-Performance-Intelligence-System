import { createFileRoute } from "@tanstack/react-router";
import { AlertTriangle } from "lucide-react";

import { PageHeader } from "@/components/page-header";

export const Route = createFileRoute("/methodology")({
  head: () => ({
    meta: [
      { title: "Methodology & Limitations — MedTrack_DV" },
      {
        name: "description",
        content:
          "How the MedTrack_DV dashboards were built, from data collection to Tableau visualisation, and their limitations.",
      },
      { property: "og:title", content: "Methodology & Limitations — MedTrack_DV" },
      {
        property: "og:description",
        content: "How the MedTrack_DV dashboards were built and their limitations.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: MethodologyPage,
});

const steps = [
  {
    title: "Data collection",
    text: "Healthcare data was gathered from [dataset source — to be added]. The dataset's fields, time period and size will be documented here.",
  },
  {
    title: "Data cleaning",
    text: "Missing values, duplicates and inconsistent formats were handled so that every record could be analysed reliably.",
  },
  {
    title: "Data transformation",
    text: "Fields were restructured and derived measures were created to support each dashboard's questions.",
  },
  {
    title: "Exploratory analysis",
    text: "Distributions, trends and relationships were explored to decide which views would be most informative.",
  },
  {
    title: "Dashboard design",
    text: "Four focused dashboards were built in Tableau with filters and interactivity, following clear visual design principles.",
  },
  {
    title: "Publishing & presentation",
    text: "The dashboards were published on Tableau Public and embedded in this website for presentation.",
  },
];

const limitations = [
  "Findings depend entirely on the quality, completeness and time period of the source dataset.",
  "If the dataset is public or sample data, it may not represent any specific real hospital.",
  "The dashboards are descriptive: they show patterns but do not prove cause and effect.",
  "Data is a static snapshot and is not updated in real time.",
  "Tableau Public dashboards are publicly visible, so no private or identifiable patient data is used.",
  "Embedded dashboards need an internet connection and may load slowly on some networks.",
];

function MethodologyPage() {
  return (
    <div className="space-y-12">
      <PageHeader
        eyebrow="Methodology & Limitations"
        title="How the dashboards were built"
        description="The project follows a standard data science workflow, moving from raw data to interactive, published dashboards."
      />

      <section>
        <ol className="relative grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {steps.map((s, i) => (
            <li key={s.title} className="rounded-2xl border bg-card p-6 shadow-card">
              <span className="font-display text-sm font-semibold text-primary">
                Step {String(i + 1).padStart(2, "0")}
              </span>
              <h3 className="mt-2 text-lg font-semibold text-foreground">{s.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{s.text}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="rounded-3xl border bg-gradient-soft p-6 md:p-10">
        <h2 className="flex items-center gap-3 text-2xl font-semibold text-foreground">
          <span className="flex size-10 items-center justify-center rounded-xl bg-gradient-primary text-primary-foreground">
            <AlertTriangle className="size-5" />
          </span>
          Limitations
        </h2>
        <ul className="mt-6 grid gap-4 md:grid-cols-2">
          {limitations.map((l) => (
            <li
              key={l}
              className="flex gap-3 rounded-xl border bg-card p-4 text-sm leading-relaxed text-muted-foreground"
            >
              <span className="mt-1.5 size-2 shrink-0 rounded-full bg-primary" />
              {l}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
