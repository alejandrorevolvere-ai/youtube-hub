#!/usr/bin/env python3
"""Tablero unico de monetizacion (A2): un solo comando, cinco fuentes.

  python scripts/monetization.py            # tablero
  python scripts/monetization.py --no-smoke # sin comprobar el sitio

Fuentes:
  - GET https://senalabierta.pages.dev/api/stats   visitas del hub (KV, publico)
  - Buttondown API (.env, BUTTONDOWN_API_KEY)      suscriptores + ultimo envio
  - Cloudflare KV via OAuth (config default.toml)  pagos de Ko-fi (prefijo kofi:)
  - scripts/smoke_site.py                          salud del sitio
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = "https://senalabierta.pages.dev"
CF_ACC = "72d97cecf2b62b411a90663527bcf513"
KV_NS = "569eb6b6d9594428859082af2119667f"
CF_CONF = Path.home() / "AppData" / "Roaming" / "xdg.config" / ".wrangler" / "config" / "default.toml"


def load_env() -> None:
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def get(url, headers=None, timeout=25):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "opencode"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", "replace")), r.status
    except urllib.error.HTTPError as e:
        return {"err": e.code, "body": e.read().decode("utf-8", "replace")[:200]}, e.code
    except Exception as e:  # noqa: BLE001
        return {"err": str(e)}, 0


def cf_token() -> str:
    try:
        toml = CF_CONF.read_text(encoding="utf-8")
    except OSError:
        return ""
    m = re.search(r'oauth_token\s*=\s*"([^"]+)"|token\s*=\s*"([^"]+)"', toml)
    return (m.group(1) or m.group(2)) if m else ""


def fetch_visitas():
    data, code = get(f"{HUB}/api/stats")
    if code != 200:
        return {"error": f"api/stats HTTP {code}"}
    hoy = date.today().isoformat()
    hoy_n = next((n for d, n in data.get("days", []) if d == hoy), 0)
    return {"total": data.get("total", 0), "hoy": hoy_n, "top": data.get("top", [])[:5]}


def fetch_buttondown():
    key = os.environ.get("BUTTONDOWN_API_KEY")
    if not key:
        return {"error": "sin BUTTONDOWN_API_KEY"}
    h = {"Authorization": f"Token {key}", "X-API-Version": "2026-04-01"}
    out = {}
    subs, code = get("https://api.buttondown.com/v1/subscribers?limit=1", h)
    out["suscriptores"] = subs.get("count", "—") if code == 200 else f"HTTP {code}"
    emails, code2 = get("https://api.buttondown.com/v1/emails?limit=20", h)
    if code2 == 200:
        enviados = [e for e in emails.get("results", []) if e.get("status") in ("sent", "resending")]
        enviados.sort(key=lambda e: e.get("creation_date") or "", reverse=True)
        out["ultimo"] = enviados[0] if enviados else None
        an = (out["ultimo"] or {}).get("analytics") or {}
        out["aperturas"] = an.get("opened") or an.get("open_count")
        out["clics"] = an.get("clicked") or an.get("click_count")
    else:
        out["ultimo"] = None
        out["emails_err"] = f"HTTP {code2}"
    return out


def fetch_kofi():
    tok = cf_token()
    if not tok:
        return {"error": "sin OAuth de Cloudflare"}
    h = {"Authorization": f"Bearer {tok}"}
    base = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACC}/storage/kv/namespaces/{KV_NS}"
    keys, code = get(f"{base}/keys?prefix=kofi:&limit=200", h)
    if code != 200 or not keys.get("success"):
        return {"error": f"KV keys HTTP {code}"}
    pagos = []
    for k in keys.get("result", []):
        val, c = get(f"{base}/values/{urllib.parse.quote(k['name'], safe='')}", h)
        if c == 200 and isinstance(val, dict) and "err" not in val:
            pagos.append(val)
    total = 0.0
    for p in pagos:
        try:
            total += float(p.get("amount") or 0)
        except (TypeError, ValueError):
            pass
    return {"pagos": len(pagos), "importe": total, "moneda": (pagos[-1].get("currency") if pagos else "EUR") or "EUR",
            "ultimo": (pagos[-1] if pagos else None)}


def fetch_smoke() -> str:
    try:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "smoke_site.py")],
                           capture_output=True, text=True, timeout=180, cwd=ROOT)
        lines = [l for l in (r.stdout or "").splitlines() if l.strip()]
        return lines[-1] if lines else "sin salida"
    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-smoke", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    load_env()

    v = fetch_visitas()
    b = fetch_buttondown()
    k = fetch_kofi()
    s = "omitido" if args.no_smoke else fetch_smoke()

    print("=" * 62)
    print("MONETIZACION — Senal Abierta  (mando unico)")
    print("=" * 62)
    print(f"{'Visitas totales (desde 01/10)':<38} {v.get('total', '—')}")
    print(f"{'Visitas hoy':<38} {v.get('hoy', '—')}")
    if v.get("top"):
        print(f"{'Top rutas':<38} " + ", ".join(f"{p} ({n})" for p, n in v["top"]))
    print("-" * 62)
    print(f"{'Suscriptores Buttondown':<38} {b.get('suscriptores', '—')}")
    if b.get("ultimo"):
        u = b["ultimo"]
        print(f"{'Ultimo envio':<38} {u.get('subject', '')[:40]}")
        print(f"{'  estado / aperturas / clics':<38} {u.get('status')} / {b.get('aperturas') or '—'} / {b.get('clics') or '—'}")
    elif b.get("emails_err"):
        print(f"{'Emails':<38} {b['emails_err']}")
    print("-" * 62)
    if k.get("error"):
        print(f"{'Ko-fi':<38} {k['error']}")
    else:
        print(f"{'Donaciones Ko-fi (webhook)':<38} {k['pagos']} pagos")
        print(f"{'  importe acumulado':<38} {k['importe']:.2f} {k['moneda']}")
        if k.get("ultimo"):
            u = k["ultimo"]
            print(f"{'  ultima':<38} {u.get('type')} {u.get('amount')} {u.get('currency')} ({str(u.get('ts'))[:19]})")
    print("-" * 62)
    print(f"{'Smoke del sitio':<38} {s}")
    if b.get("error"):
        print(f"{'Buttondown':<38} {b['error']}")
    if v.get("error"):
        print(f"{'api/stats':<38} {v['error']}")
    print("=" * 62)
    print("Pendientes (ventanas del usuario): PayPal en Ko-fi, GSC, Amazon IBAN,")
    print("ElevenLabs/NordVPN, /legal. Ver promo/flywheel.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
