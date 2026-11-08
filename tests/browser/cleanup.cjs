const { rmSync } = require("node:fs");
module.exports = async (config) =>
  rmSync(config.metadata.demoTempDirectory, { recursive: true, force: true });
