import { createFileRoute } from "@tanstack/react-router";

import { DashboardView } from "@/components/dashboard-view";

export const Route = createFileRoute("/hospital-overview")({
  head: () => ({
    meta: [
      { title: "Hospital Overview — MedTrack_DV" },
      { name: "description", content: "Hospital Overview Tableau dashboard in MedTrack_DV." },
      { property: "og:title", content: "Hospital Overview — MedTrack_DV" },
      { property: "og:description", content: "Hospital Overview Tableau dashboard in MedTrack_DV." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: HospitalOverviewPage,
});

function HospitalOverviewPage() {
  return <DashboardView path="/hospital-overview" />;
}
