import { expect, test } from "@playwright/test";

test("renders JurisAI, login and protects dashboard", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("JurisAI")).toBeVisible();

  await page.goto("/login");
  await expect(page.getByText("Entrar no JurisAI")).toBeVisible();

  await page.goto("/dashboard");
  await expect(page).toHaveURL(/\/login/);
});
