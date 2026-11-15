const { test, expect } = require("@playwright/test");

test("a failed refresh after a conflict preserves input and keeps the form usable", async ({
  page,
}) => {
  const scriptErrors = [];
  page.on("pageerror", (error) => scriptErrors.push(error.message));
  await page.goto("/");
  await expect(page.locator("#rows button").first()).toBeVisible();

  const form = page.locator("#detail form").first();
  const note = form.locator("textarea").first();
  if (await note.count())
    await note.fill("Preserve this fictional review note");
  await page.route("**/api/action", (route) =>
    route.fulfill({
      status: 409,
      contentType: "application/json",
      body: JSON.stringify({ error: "This record changed." }),
    }),
  );
  await page.route("**/api/snapshot", (route) => route.abort());
  await form.getByRole("button").click();
  await expect(page.getByRole("alert")).toContainText("could not refresh");
  await expect(form.getByRole("button")).toBeEnabled();
  if (await note.count())
    await expect(note).toHaveValue("Preserve this fictional review note");
  expect(scriptErrors).toEqual([]);
});
