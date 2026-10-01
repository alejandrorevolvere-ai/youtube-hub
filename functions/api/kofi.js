// Receptor del webhook de Ko-fi: valida el verification_token, registra el
// pago en KV (prefijo "kofi:") y responde 200 (Ko-fi reintenta si no lo
// recibe). GET ?limit=N devuelve la lista de pagos (para dashboards/n8n).
// El token vive en KV (`secret:kofi_token`, escrito via API CF,
// nunca en git) con fallback a la env-var KOFI_TOKEN del proyecto Pages.
// No se guarda email ni otros PII; si is_public es false tampoco nombre/mensaje.
function json(status, obj) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}

async function listPagos(env, limit) {
  const out = [];
  let cursor;
  do {
    const page = await env.VISITS.list({ prefix: "kofi:", cursor });
    for (const k of page.keys) {
      const raw = await env.VISITS.get(k.name);
      if (raw) {
        try {
          const rec = JSON.parse(raw);
          rec.id = k.name.slice(5);
          out.push(rec);
        } catch (_) {}
      }
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor && out.length < limit + 50);
  out.sort((a, b) => (a.id < b.id ? 1 : -1));
  return out.slice(0, limit);
}

export const onRequest = async ({ request, env }) => {
  if (request.method === "GET") {
    const url = new URL(request.url);
    const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "100", 10) || 100, 1), 500);
    const payments = await listPagos(env, limit);
    return json(200, { count: payments.length, payments });
  }
  if (request.method !== "POST") return json(405, { error: "method not allowed" });
  const expected = env.KOFI_TOKEN || (env.VISITS && (await env.VISITS.get("secret:kofi_token")));
  if (!expected) return json(503, { error: "token de Ko-fi no configurado" });

  let payload;
  try {
    const form = await request.formData();
    const raw = form.get("data");
    payload = typeof raw === "string" ? JSON.parse(raw) : null;
  } catch (_) {
    return json(400, { error: "body invalido" });
  }
  if (!payload || payload.verification_token !== expected) {
    return json(403, { error: "verification_token invalido" });
  }

  const pub = payload.is_public === true || payload.is_public === "true";
  const rec = {
    type: payload.type || null,
    amount: payload.amount || null,
    currency: payload.currency || null,
    tier: payload.tier_name || null,
    msg: payload.message_id || null,
    public: pub,
    ts: payload.timestamp || new Date().toISOString(),
  };
  if (pub) {
    rec.from = payload.from_name || null;
    if (payload.message) rec.note = String(payload.message).slice(0, 500);
  }
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  await env.VISITS.put("kofi:" + stamp + "-" + (rec.msg || "x"), JSON.stringify(rec));
  return json(200, { ok: true });
};
