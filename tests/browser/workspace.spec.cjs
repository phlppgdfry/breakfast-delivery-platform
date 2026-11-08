const { test, expect } = require("@playwright/test");

test("workspace, branding and export load without script errors", async ({
  page,
  request,
}) => {
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await expect(page.locator("#rows button").first()).toBeVisible();
  await expect(page.locator("#notice")).toBeEmpty();
  await expect(page.locator("#brand img")).toHaveJSProperty("complete", true);
  expect(
    await page.locator("#brand img").evaluate((img) => img.naturalWidth),
  ).toBeGreaterThan(0);
  await expect(page.locator("link[rel=icon]")).toHaveAttribute(
    "href",
    "/favicon.svg",
  );
  for (const asset of [
    "/favicon.svg",
    "/logo.svg",
    "/apple-touch-icon.png",
    "/site.webmanifest",
    "/social-preview.png",
  ]) {
    const response = await request.get(asset);
    expect(response.status(), asset).toBe(200);
    expect((await response.body()).length).toBeGreaterThan(50);
  }
  const exported = await request.get("/api/export.csv");
  expect(exported.status()).toBe(200);
  expect(await exported.text()).toContain("id,");
  expect(errors).toEqual([]);
});

test("search, empty state and status filter respond", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#rows button").first()).toBeVisible();
  await page.getByLabel("Search", { exact: true }).fill("no-such-record");
  await expect(page.locator("#rows")).toContainText("No matching records.");
  await page.getByLabel("Search", { exact: true }).fill("");
  const status = await page
    .locator("#filter option")
    .nth(1)
    .getAttribute("value");
  // Options use text as their value when no explicit value attribute is present.
  const selected =
    status || (await page.locator("#filter option").nth(1).innerText());
  await page.getByLabel("Status", { exact: true }).selectOption(selected);
  const statuses = await page.locator("#rows .status").allTextContents();
  expect(statuses.length).toBeGreaterThan(0);
  expect(statuses.every((value) => value === selected)).toBe(true);
});

for (const width of [390, 768, 1440]) {
  test(`responsive workspace at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/");
    await expect(page.locator("#rows button").first()).toBeVisible();
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth),
    ).toBeLessThanOrEqual(width);
    await page.locator("#rows button").first().click();
    await expect(page.locator("#detail h2").first()).toBeVisible();
  });
}

test("reserve, fulfil and reject an over-capacity order", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#rows button").first()).toBeVisible();
  await page
    .getByLabel("Customer name · fictional only", { exact: true })
    .fill("Taylor Demo");
  await page.getByLabel("Number of boxes", { exact: true }).fill("3");
  await page
    .getByLabel("I have reviewed the allergens listed above", { exact: true })
    .check();
  await page
    .getByRole("button", { name: "Reserve breakfast box", exact: true })
    .click();
  await expect(page.locator("#notice")).toContainText("Reservation confirmed");
  await expect(page.locator("#detail")).toContainText("€37.50");
  await page
    .getByRole("button", { name: "Start preparation", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Hand to delivery partner", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Confirm delivery", exact: true })
    .click();
  await expect(page.locator("#detail")).toContainText("Delivered");
  await page
    .getByLabel("Customer name · fictional only", { exact: true })
    .fill("Capacity Test");
  await page
    .getByLabel("I have reviewed the allergens listed above", { exact: true })
    .check();
  await page
    .getByRole("button", { name: "Reserve breakfast box", exact: true })
    .click();
  await expect(page.locator("#notice")).toContainText(
    "insufficient box capacity",
  );
  await page.reload();
  await expect(page.locator("#rows")).toContainText("Taylor Demo");
  await expect(page.locator("#rows")).toContainText("Delivered");
});
