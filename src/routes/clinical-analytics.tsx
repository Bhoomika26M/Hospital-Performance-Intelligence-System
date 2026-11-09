import { createFileRoute } from "@tanstack/react-router";

import { DashboardView } from "@/components/dashboard-view";

export const Route = createFileRoute("/clinical-analytics")({
  head: () => ({
    meta: [
      { title: "Clinical Analytics — MedTrack_DV" },
      { name: "description", content: "Clinical Analytics Tableau dashboard in MedTrack_DV." },
      { property: "og:title", content: "Clinical Analytics — MedTrack_DV" },
      {
        property: "og:description",
        content: "Clinical Analytics Tableau dashboard in MedTrack_DV.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: ClinicalAnalyticsPage,
});

function ClinicalAnalyticsPage() {
  return <DashboardView path="/clinical-analytics" />;
}
