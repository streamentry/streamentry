"use strict";

const assert = require("assert/strict");
const fs = require("fs");
const os = require("os");
const path = require("path");
const extractZip = require("extract-zip");

async function main() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "streamentry-extract-zip-"));
  try {
    const archive = path.join(root, "untrusted.zip");
    const output = path.join(root, "output");
    fs.writeFileSync(archive, "not opened by the disabled fallback");
    await assert.rejects(
      extractZip(archive, { dir: output }),
      /fallback is disabled/i,
    );
    assert.equal(fs.existsSync(output), false);
    console.log("safe-extract-zip: legacy fallback rejected without writing");
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
