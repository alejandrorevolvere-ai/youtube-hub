# Señal Abierta

Sitio estático del hub editorial **Señal Abierta** — presentación de los canales
[El Club del Negocio](https://www.youtube.com/@historiasdenegocios-o5m) e
[IA en 60 segundos](https://www.youtube.com/@IAen60-f1i).

**En vivo:** https://senalabierta.pages.dev/ (Cloudflare Pages)

## Estructura

| Archivo | Función |
|---|---|
| `index.html` | Hub principal (hero, canales, últimos vídeos, manifiesto, hitos) |
| `v/<slug>/index.html` | Landing SEO por vídeo (generada, no editar a mano) |
| `archivo/index.html` | Archivo completo filtrable por canal (generado) |
| `404.html` | Página no encontrada (la sirve Cloudflare Pages) |
| `styles.css` | Diseño editorial + fuentes auto-alojadas (`fonts/`) |
| `app.js` | Reveal, count-up, tarjetas, buscador y "vídeo aleatorio" |
| `archivo.js` | Filtros y búsqueda del archivo |
| `landing.js` | Reproductor facade (click → iframe youtube-nocookie) |
| `data.json` | Datos de canales (generado, no editar a mano) |
| `v-index.json` | Índice ligero id/slug/título (generado) |
| `feed.xml` | Feed Atom de los 15 últimos vídeos (generado) |
| `img/hitos/` | Imágenes de la línea de tiempo (duotone, self-hosted) |
| `content/videos.json` | Archivo acumulativo de vídeos (generado) |
| `og.png`, `favicon.svg` | Preview para redes y favicon |
| `sitemap.xml`, `robots.txt`, `llms.txt` | SEO |
| `_headers` | CSP + cabeceras de seguridad (generado, Cloudflare Pages) |
| `scripts/fetch_channel_data.py` | Regenera `data.json` y `content/videos.json` |
| `scripts/build_pages.py` | Genera fichas, archivo, feed, v-index, sitemap y llms.txt |
| `scripts/fetch_hitos.py` | Descarga imágenes PD/CC0 de Commons y las pasa a duotone |
| `scripts/csp_hashes.py` | Regenera la CSP (meta de index.html + `_headers`) |
| `scripts/package_site.py` | Empaqueta `dist/` con solo lo público (previo al deploy) |
| `promo/promo.md` | Textos de promoción listos para pegar |

### Monetización

- Amazon Afiliados: tag `senalabierta-21` ya enchufado en `AFFILIATES`
  (`scripts/build_pages.py`); pendientes de alta: Quipu, ElevenLabs y
  NordVPN (slots `TODO-AFILIADO`).
- Footer del hub: Ko-fi (`ko-fi.com/alejandrorevolvere`) y Buttondown
  (`buttondown.com/revolvere`) configurados en `index.html`.

## Actualizar contenido y redesplegar

```powershell
$env:YT_TOKEN_PICKLE = "<ruta local a tu token OAuth de YouTube>"
python scripts/fetch_channel_data.py
python scripts/build_pages.py
python scripts/csp_hashes.py        # solo si tocaste un <script> inline
python scripts/package_site.py      # empaqueta dist/ (lo único público)
npx wrangler pages deploy dist --project-name senalabierta --branch=main --commit-dirty=true
```

`wrangler pages deploy` no respeta `.cfignore`/`.assetsignore`, por eso el
filtro vive en `scripts/package_site.py`: `dist/` solo contiene lo público
(nunca `scripts/`, `promo/`, `content/`, `.git*`).

Sin `YT_TOKEN_PICKLE`, las estadísticas se conservan del `data.json` anterior
(solo se actualizan los vídeos vía RSS). **El token nunca se copia al repo.**

## Despliegue

- **Producción:** Cloudflare Pages clásico, proyecto `senalabierta`
  (https://senalabierta.pages.dev/), deploy con wrangler desde local; el
  directorio `dist/` es la única fuente de assets.
- **Respaldo de código:** repo GitHub (`main`), sin conexión con Cloudflare.
- **URL antigua** `alejandrorevolvere-ai.github.io/youtube-hub/`: sirve un
  stub con redirect a la nueva URL desde el branch `gh-pages` (canonical +
  `noindex` + JS que conserva query/hash para no romper UTM antiguos).

## Seguridad

- CSP estricta (`default-src 'none'`) con hashes, servida también como header
  HTTP real vía `_headers` (incluye `frame-ancestors 'none'`).
- `app.js`/`landing.js`/`archivo.js` construyen el DOM solo con
  `textContent`/`createElement` (sin `innerHTML`).
- Credenciales excluidas por `.gitignore` (`*.pickle`, `.env`, `config/`).
- La única URL externa permitida en el player es `youtube-nocookie.com`.
