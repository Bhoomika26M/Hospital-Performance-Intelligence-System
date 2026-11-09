import { describe, expect, it } from "vitest";

import { DASHBOARDS, toTableauEmbedUrl } from "@/lib/dashboards";

describe("Tableau Public embed links", () => {
  it("shows a placeholder (no embed) when no link is provided", () => {
    expect(toTableauEmbedUrl("")).toBeNull();
    expect(toTableauEmbedUrl("   ")).toBeNull();
  });

  it("converts a /views/ share link into an embed link", () => {
    expect(
      toTableauEmbedUrl("https://public.tableau.com/views/MedTrack/HospitalOverview?:language=en-US"),
    ).toBe(
      "https://public.tableau.com/views/MedTrack/HospitalOverview?:showVizHome=no&:embed=true&:toolbar=yes&:tabs=no",
    );
  });

  it("converts a profile /viz/ link into an embed link", () => {
    expect(
      toTableauEmbedUrl("https://public.tableau.com/app/profile/someone/viz/MedTrack/PatientFlow"),
    ).toBe(
      "https://public.tableau.com/views/MedTrack/PatientFlow?:showVizHome=no&:embed=true&:toolbar=yes&:tabs=no",
    );
  });

  it("rejects links that are not from Tableau Public", () => {
    expect(toTableauEmbedUrl("https://example.com/views/MedTrack/PatientFlow")).toBeNull();
  });

  it("connects each dashboard page to its own Tableau view", () => {
    const views = Object.fromEntries(
      DASHBOARDS.map((d) => [d.path, toTableauEmbedUrl(d.tableauUrl)?.split("?")[0]]),
    );
    const base = "https://public.tableau.com/views/MEDTRACK_DV_Hospital_Analytics";
    expect(views).toEqual({
      "/hospital-overview": `${base}/HospitalOverview`,
      "/patient-flow": `${base}/PatientFlow`,
      "/clinical-analytics": `${base}/ClinicalAnalytics`,
      "/resource-utilization": `${base}/ResourceUtilization`,
    });
  });

  it("lists exactly the four project dashboards", () => {
    expect(DASHBOARDS.map((d) => d.title)).toEqual([
      "Hospital Overview",
      "Patient Flow",
      "Clinical Analytics",
      "Resource Utilization",
    ]);
  });
});
