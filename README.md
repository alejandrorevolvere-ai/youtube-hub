# Señal Abierta

Sitio estático del hub editorial **Señal Abierta** — presentación de los canales
[El Club del Negocio](https://www.youtube.com/@historiasdenegocios-o5m) e
[IA en 60 segundos](https://www.youtube.com/@IAen60-f1i).

**En vivo:** https://senalabierta.pages.dev/ (Cloudflare Pages)

## Estructura

| Archivo | Función |
|---|---|
| `index.html` | Hub principal (hero, canales, últimos vídeos, manifiesto) |
| `v/<slug>/index.html` | Landing SEO por vídeo (generada, no editar a mano) |
| `styles.css` | Diseño editorial + fuentes auto-alojadas (`fonts/`) |
| `app.js` | Reveal, count-up y refresco de tarjetas desde `data.json` |
| `landing.js` | Reproductor facade (click → iframe youtube-nocookie) |
| `data.json` | Datos de canales (generado, no editar a mano) |
| `content/videos.json` | Archivo acumulativo de vídeos (generado) |
| `og.png`, `favicon.svg` | Preview para redes y favicon |
| `sitemap.xml`, `robots.txt`, `llms.txt` | SEO |
| `_headers` | CSP + cabeceras de seguridad (generado, Cloudflare Pages) |
| `scripts/fetch_channel_data.py` | Regenera `data.json` y `content/videos.json` |
| `scripts/build_pages.py` | Genera fichas `/v/<slug>/`, sitemap y llms.txt |
| `scripts/csp_hashes.py` | Regenera la CSP (meta de index.html + `_headers`) |
| `promo/promo.md` | Textos de promoción listos para pegar |

## Actualizar contenido y redesplegar

```powershell
$env:YT_TOKEN_PICKLE = "<ruta local a tu token OAuth de YouTube>"
python scripts/fetch_channel_data.py
python scripts/build_pages.py
python scripts/csp_hashes.py        # solo si tocaste un <script> inline
npx wrangler pages deploy . --project-name senalabierta --branch=main
```

Sin `YT_TOKEN_PICKLE`, las estadísticas se conservan del `data.json` anterior
(solo se actualizan los vídeos vía RSS). **El token nunca se copia al repo.**

## Despliegue

Cloudflare Pages (proyecto `senalabierta`), deploy directo con wrangler desde
local. El repo de GitHub es copia de seguridad del código; no está enlazado
con Cloudflare. Antigua URL `alejandrorevolvere-ai.github.io/youtube-hub/`
redirige a la nueva desde el branch `gh-pages`.

## Seguridad

- CSP estricta (`default-src 'none'`) con hashes, servida también como header
  HTTP real vía `_headers` (incluye `frame-ancestors 'none'`).
- `app.js`/`landing.js` construyen el DOM solo con `textContent`/`createElement`.
- Credenciales excluidas por `.gitignore` (`*.pickle`, `.env`, `config/`).
- La única URL externa permitida en el player es `youtube-nocookie.com`.
