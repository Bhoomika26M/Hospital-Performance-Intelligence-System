import { createFileRoute } from "@tanstack/react-router";

import { DashboardView } from "@/components/dashboard-view";

export const Route = createFileRoute("/resource-utilization")({
  head: () => ({
    meta: [
      { title: "Resource Utilization — MedTrack_DV" },
      { name: "description", content: "Resource Utilization Tableau dashboard in MedTrack_DV." },
      { property: "og:title", content: "Resource Utilization — MedTrack_DV" },
      {
        property: "og:description",
        content: "Resource Utilization Tableau dashboard in MedTrack_DV.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: ResourceUtilizationPage,
});

function ResourceUtilizationPage() {
  return <DashboardView path="/resource-utilization" />;
}
