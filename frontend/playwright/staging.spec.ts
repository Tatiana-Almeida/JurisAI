import { expect, test } from "@playwright/test";

const baseUrl = process.env.E2E_STAGING_BASE_URL?.trim();

test.describe("staging smoke", () => {
  test.skip(!baseUrl, "E2E_STAGING_BASE_URL nao configurado para smoke de staging.");

  test("renders public pages and keeps protected modules behind auth", async ({ page }) => {
    await page.goto(baseUrl!);
    await expect(page.getByText("JurisAI")).toBeVisible();

    await page.goto(new URL("/login", baseUrl!).toString());
    await expect(page.getByText("Entrar no JurisAI")).toBeVisible();

    await page.goto(new URL("/dashboard", baseUrl!).toString());
    await expect(page).toHaveURL(/\/login/);

    await page.goto(new URL("/clients", baseUrl!).toString());
    await expect(page).toHaveURL(/\/login/);

    await page.goto(new URL("/cases", baseUrl!).toString());
    await expect(page).toHaveURL(/\/login/);

    await page.goto(new URL("/documents", baseUrl!).toString());
    await expect(page).toHaveURL(/\/login/);
  });
});
