import { expect, test } from "@playwright/test";

test("renders JurisAI on home and login", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("JurisAI")).toBeVisible();

  await page.goto("/login");
  await expect(page.getByText("Entrar no JurisAI")).toBeVisible();
});
