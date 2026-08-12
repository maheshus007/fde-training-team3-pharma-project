import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Avoid flaky Windows rename races against a half-written `.next` tree.
  distDir: ".next-build",
};

export default nextConfig;
