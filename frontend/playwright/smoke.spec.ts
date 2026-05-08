import { expect, test } from "@playwright/test";

test("renders JurisAI, login and protects private modules", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("JurisAI")).toBeVisible();

  await page.goto("/login");
  await expect(page.getByText("Entrar no JurisAI")).toBeVisible();

  for (const path of [
    "/dashboard",
    "/clients",
    "/cases",
    "/documents",
    "/ocr",
    "/knowledge-base",
    "/deadlines",
    "/calendar",
    "/finance",
    "/billing",
    "/settings",
    "/client-portal",
  ]) {
    await page.goto(path);
    await expect(page).toHaveURL(/\/login/);
  }
});
