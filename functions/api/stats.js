// Contador de visitas propio (A11): /api/stats
//   POST {p: "/ruta"} -> incrementa el dia (UTC) y la ruta en KV
//   GET               -> {total, days:[[fecha,n]], top:[[ruta,n]]}
// Debe servirse SIN cache (yo lo leo cada semana). Sin PII: no se guarda
// IP, UA ni cookies; solo contador diario y por ruta.
const DAY_RE = /^\d{4}-\d{2}-\d{2}$/;

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Robots-Tag": "noindex",
    },
  });
}

async function incr(env, key) {
  const n = Number(await env.VISITS.get(key)) || 0;
  await env.VISITS.put(key, String(n + 1));
}

async function onPost(request, env) {
  const ua = request.headers.get("user-agent") || "";
  if (/bot|crawl|spider|slurp|preview|monitor|lighthouse/i.test(ua)) {
    return new Response(null, { status: 204 });
  }
  let path = "/";
  try {
    const body = await request.json();
    if (body && typeof body.p === "string") path = body.p.slice(0, 300);
  } catch (_) {}
  const today = new Date().toISOString().slice(0, 10);
  await Promise.all([incr(env, "d:" + today), incr(env, "p:" + path)]);
  return json({ ok: true });
}

async function onGet(env) {
  const now = Date.now();
  const dayKeys = [];
  for (let i = 0; i < 30; i++) {
    dayKeys.push("d:" + new Date(now - i * 86400000).toISOString().slice(0, 10));
  }
  const dayVals = await Promise.all(dayKeys.map((k) => env.VISITS.get(k)));
  const days = [];
  let total = 0;
  for (let i = 0; i < dayKeys.length; i++) {
    const n = Number(dayVals[i]) || 0;
    if (n > 0) {
      days.push([dayKeys[i].slice(2), n]);
      total += n;
    }
  }
  const list = await env.VISITS.list({ prefix: "p:", limit: 200 });
  const pathVals = await Promise.all(list.keys.map((k) => env.VISITS.get(k.name)));
  const top = [];
  for (let i = 0; i < list.keys.length; i++) {
    const n = Number(pathVals[i]) || 0;
    if (n > 0) top.push([list.keys[i].name.slice(2), n]);
  }
  top.sort((a, b) => b[1] - a[1]);
  return json({
    total,
    days,
    top: top.slice(0, 25),
    fetchedAt: new Date().toISOString(),
    scope: "visitas desde el despliegue del contador (2026-10-01), dias UTC",
  });
}

export const onRequest = async ({ request, env }) => {
  if (!env.VISITS) return json({ error: "KV VISITS no vinculada" }, 500);
  if (request.method === "POST") return onPost(request, env);
  if (request.method === "GET") return onGet(env);
  return json({ error: "method not allowed" }, 405);
};
