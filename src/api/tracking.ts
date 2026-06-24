import { createServerFn } from "@tanstack/react-start";
import * as fs from "fs";
import * as path from "path";

interface AnalyticsData {
  visits: {
    date: string;
    timestamp: number;
    path: string;
  }[];
}

export const trackPageView = createServerFn({ method: "POST" })
  .inputValidator((data: { path: string }) => data)
  .handler(async ({ data }) => {
    try {
      const isProd = process.env.NODE_ENV === "production";
      const dataDir = isProd
        ? path.join(process.cwd(), "dist", "client", "blog_data")
        : path.join(process.cwd(), "public", "blog_data");

      if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
      }

      const filePath = path.join(dataDir, "analytics.json");
      let analytics: AnalyticsData = { visits: [] };

      if (fs.existsSync(filePath)) {
        try {
          analytics = JSON.parse(fs.readFileSync(filePath, "utf-8"));
        } catch (e) {}
      }

      analytics.visits.push({
        date: new Date().toISOString().split("T")[0],
        timestamp: Date.now(),
        path: data.path,
      });

      if (analytics.visits.length > 10000) {
        analytics.visits = analytics.visits.slice(-10000);
      }

      fs.writeFileSync(filePath, JSON.stringify(analytics, null, 2));
      return { success: true };
    } catch (error) {
      console.error("Error tracking page view:", error);
      return { success: false };
    }
  });

export const getAnalyticsData = createServerFn({ method: "GET" }).handler(async () => {
  try {
    const isProd = process.env.NODE_ENV === "production";
    const dataDir = isProd
      ? path.join(process.cwd(), "dist", "client", "blog_data")
      : path.join(process.cwd(), "public", "blog_data");

    const filePath = path.join(dataDir, "analytics.json");

    if (!fs.existsSync(filePath)) {
      return { visits: [] };
    }

    return JSON.parse(fs.readFileSync(filePath, "utf-8")) as AnalyticsData;
  } catch (error) {
    console.error("Error fetching analytics:", error);
    return { visits: [] };
  }
});
