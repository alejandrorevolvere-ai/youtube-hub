# Señal Abierta

Sitio estático del hub editorial **Señal Abierta** — presentación de los canales
[El Club del Negocio](https://www.youtube.com/@historiasdenegocios-o5m) e
[IA en 60 segundos](https://www.youtube.com/@IAen60-f1i).

**En vivo:** https://alejandrorevolvere-ai.github.io/youtube-hub/

## Estructura

| Archivo | Función |
|---|---|
| `index.html` | Página única (hero, canales, últimos vídeos, manifiesto) |
| `styles.css` | Diseño editorial + fuentes auto-alojadas (`fonts/`) |
| `app.js` | Reveal, count-up y refresco de tarjetas desde `data.json` |
| `data.json` | Datos reales de canales (generado, no editar a mano) |
| `og.png`, `favicon.svg` | Preview para redes y favicon |
| `sitemap.xml`, `robots.txt`, `llms.txt` | SEO |
| `scripts/fetch_channel_data.py` | Regenera `data.json` |
| `scripts/csp_hashes.py` | Regenera los hashes sha256 de la CSP |
| `promo/promo.md` | Textos de promoción listos para pegar |

## Actualizar los datos

```powershell
$env:YT_TOKEN_PICKLE = "<ruta local a tu token OAuth de YouTube>"
python scripts/fetch_channel_data.py
git add data.json && git commit -m "refresh data" && git push
```

Sin `YT_TOKEN_PICKLE`, las estadísticas se conservan del `data.json` anterior
(solo se actualizan los vídeos vía RSS). **El token nunca se copia al repo.**

## Editar el HTML

La CSP exige un hash sha256 por cada `<script>` inline. Después de tocar un
script inline (el de clase `js` o un bloque JSON-LD):

```powershell
python scripts/csp_hashes.py
```

Pega el `script-src` que imprime en la meta `Content-Security-Policy` del `<head>`.

## Seguridad

- CSP estricta (`default-src 'none'`) con hashes; cero terceros (sin Google Fonts).
- `app.js` construye el DOM solo con `textContent`/`createElement` (sin `innerHTML`).
- Credenciales excluidas por `.gitignore` (`*.pickle`, `.env`, `config/`).
