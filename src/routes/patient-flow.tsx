import { createFileRoute } from "@tanstack/react-router";

import { DashboardView } from "@/components/dashboard-view";

export const Route = createFileRoute("/patient-flow")({
  head: () => ({
    meta: [
      { title: "Patient Flow — MedTrack_DV" },
      { name: "description", content: "Patient Flow Tableau dashboard in MedTrack_DV." },
      { property: "og:title", content: "Patient Flow — MedTrack_DV" },
      { property: "og:description", content: "Patient Flow Tableau dashboard in MedTrack_DV." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: PatientFlowPage,
});

function PatientFlowPage() {
  return <DashboardView path="/patient-flow" />;
}
