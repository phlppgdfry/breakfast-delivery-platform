const { defineConfig } = require("@playwright/test");
const { mkdtempSync } = require("node:fs");
const { tmpdir } = require("node:os");
const { join } = require("node:path");
const directory = mkdtempSync(
  join(tmpdir(), "breakfast-delivery-platform-e2e-"),
);
module.exports = defineConfig({
  testDir: "./tests/browser",
  workers: 1,
  retries: 0,
  timeout: 30000,
  use: {
    baseURL: "http://127.0.0.1:9115",
    browserName: "chromium",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  metadata: { demoTempDirectory: directory },
  globalTeardown: require.resolve("./tests/browser/cleanup.cjs"),
  webServer: {
    command: `python3 -m demo.server --port 9115 --db "${join(directory, "demo.sqlite3")}"`,
    url: "http://127.0.0.1:9115/api/health",
    reuseExistingServer: false,
    timeout: 15000,
    stderr: "ignore",
  },
});
