import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    css: true,
    include: ["tests/**/*.{test,spec}.{ts,tsx}"],
    exclude: ["node_modules/**", ".next/**", "playwright/**", "playwright.config.ts"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname),
    },
  },
});
