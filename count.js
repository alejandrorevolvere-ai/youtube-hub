/* Contador propio de visitas: beacon a /api/stats (sin cookies ni PII). */
try {
  fetch("/api/stats", {
    method: "POST",
    keepalive: true,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ p: location.pathname }),
  }).catch(function () {});
} catch (e) {}
