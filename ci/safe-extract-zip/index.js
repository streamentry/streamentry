"use strict";

module.exports = function rejectLegacyZipFallback() {
  return Promise.reject(
    new Error(
      "Legacy extract-zip fallback is disabled; reject the archive when the primary ZIP reader fails.",
    ),
  );
};
