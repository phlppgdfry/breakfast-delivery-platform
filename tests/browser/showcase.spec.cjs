const { test, expect } = require("@playwright/test");

test("public showcase has working branding, screenshots, navigation and mobile layout", async ({
  page,
}) => {
  await page.goto("http://127.0.0.1:9215/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.locator("link[rel=icon]")).toHaveAttribute(
    "href",
    "favicon.svg",
  );
  await expect(page.locator(".preview img")).toHaveJSProperty("complete", true);
  expect(
    await page.locator(".preview img").evaluate((img) => img.naturalWidth),
  ).toBeGreaterThan(0);
  await page.getByRole("link", { name: "Run the demo", exact: true }).click();
  await expect(page.locator("#run")).toBeInViewport();
  await expect(page.locator("#run")).toContainText("python3 -m demo.server");
  for (const width of [390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth),
    ).toBeLessThanOrEqual(width);
  }
});
