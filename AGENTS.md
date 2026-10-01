# AGENTS.md — Monetización de Señal Abierta (instrucciones para agentes)

OBJETIVO: Integrar la monetización de Señal Abierta en el flujo habitual de
subida de contenido. Trabaja en español. Ejecuta por fases y verifica cada una.

CONTEXTO
- Hub: `C:\Users\Alejandro\omnirush.ai\youtube-hub` (https://senalabierta.pages.dev/)
- Pipeline de subida: `D:\WSL\youtube-automation` (tokens: `config/youtube_token.pickle`
  = canal club, `config/youtube_token_ia.pickle` = canal ia60; NUNCA tocar/commitear).
- Canales: "club" = El Club del Negocio (@historiasdenegocios-o5m),
  "ia60" = IA en 60 segundos (@IAen60-f1i).
- Checklist semanal maestro: `<hub>\promo\flywheel.md` (léelo primero).
- Afiliados activos: Amazon tag `senalabierta-21`, Ko-fi
  `ko-fi.com/alejandrorevolvere`, Newsletter `buttondown.com/revolvere`.

## Fase 1 — CTA en descripciones de cada video nuevo (tras cada subida)

1. Tras publicar cualquier video, ejecutar desde el hub:
   ```
   python scripts\sync_video_descriptions.py --channel club   (o ia60)
   ```
   Es dry-run por defecto: comprueba que el video nuevo aparece con
   `updates=1` y el bloque CTA (hub + newsletter + Ko-fi). Si aparece,
   repetir con `--apply --limit 5`.
2. El script es idempotente (marcadores `buttondown.com/revolvere` y
   `utm_medium=description`); NUNCA correr `--apply` dos veces seguidas sin
   revisar la salida.
3. Cuota: update = 50 u, insert = 1600 u, límite 10.000/día (resetea 00:00 PT).
   Si ese día ya hubo subidas y quedan <1.000 unidades, NO aplicar: deja el
   dry-run y reanuda al día siguiente.

## Fase 2 — Libro por video (solo canal club, si el video tiene libro asociado)

1. ANTES de Fase 1, añadir el id del video en `<hub>\data\libros.json`
   (array `videos` del libro correspondiente; si no existe, crear la entrada
   con asin/title/empresa — confirmar ASIN con Alejandro antes de publicar).
2. Reconstruir el sitio:
   ```
   python scripts\fetch_channel_data.py
   python scripts\build_pages.py
   python scripts\csp_hashes.py
   python scripts\smoke_site.py     # debe decir ALL OK (42 checks)
   python scripts\package_site.py
   npx wrangler pages deploy dist --project-name senalabierta --branch=main --commit-dirty=true
   ```
3. Verificar en vivo: la landing del video contiene su ASIN y
   `rel="sponsored"`; `/libros/` cuenta sus fichas.
4. Reglas: nunca editar a mano `v/`, `archivo/`, `libros/` (son generados);
   `dist/` solo con `package_site.py`; NO tocar `.env` ni `.env.example`.

## Fase 3 — Comentario fijado en cada video nuevo

Plantilla de `<hub>\promo\promo.md` §4, con `utm_medium=pinned_comment`. Si el
video tiene libro, añadir debajo el enlace Amazon con
`utm_medium=pinned_comment` + la divulgación:
"Como Afiliado de Amazon, percibo dinero con las compras que cumplen los
requisitos."

## Fase 4 — Newsletter semanal (los lunes)

1. `python scripts\newsletter_draft.py` → revisa `<hub>\promo\digest-AAAA-WW.md`
2. `python scripts\newsletter_draft.py --apply` → crea DRAFT en Buttondown.
3. PROHIBIDO enviar/publicar: solo borrador. Alejandro lo revisa y publica
   a mano. La clave está en `<hub>\.env` (`BUTTONDOWN_API_KEY`): no la
   imprimas, no la guardes en otro sitio, no la commitees.

## Límites inquebrantables

- Nunca re-subir un video (marcador `.seo.uploaded`); nunca borrar videos.
- Nunca subir ni re-subir con quota <1600 libres.
- Tokens solo en `D:\WSL\youtube-automation\config\`.
- Sin cambios fuera de: `<hub>` (monetización) y las fases de inspección
  del pipeline de subida.
- Si algo falla: para, reporta qué falló y espera confirmación.

## Definición de éxito

- Tras una subida: descripción con bloque CTA verificada vía API,
  smoke `ALL OK`, deploy con 200 en vivo, y un dry-run de newsletter en `promo/`.
