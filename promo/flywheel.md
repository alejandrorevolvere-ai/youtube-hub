# Flywheel semanal — YouTube ↔ Hub ↔ Newsletter ↔ Ko-fi ↔ Amazon

El loop: **vídeo nuevo → descripción con CTA → hub → newsletter → libro →
3 ventas de Amazon → aprobación del programa**.

## Cada lunes (≈15 min)

- [x] `python scripts/newsletter_draft.py` → revisar `promo/digest-AAAA-WW.md`
      (W40: 22 estrenos, 01/10/2026)
- [x] `python scripts/newsletter_draft.py --apply` → enviar desde Buttondown
      (W40 enviado por API: draft `em_08b5ajxeer8jg83yq2c4hb9ct8` → status
      `sent`; 0 suscriptores, ver archivo público del botón)
- [ ] Comentario fijado en el vídeo nuevo (`promo.md` §4)
- [ ] Compartir el vídeo + hub en X/TikTok con UTM (`promo.md` §1)

## Con cada vídeo nuevo (pipeline normal)

- [ ] Subir vídeo (pipeline `D:\WSL\youtube-automation`)
- [ ] `python scripts/sync_video_descriptions.py --channel club|ia60`
      (CTA hub/newsletter/Ko-fi automático)
- [ ] Si es del Club y tiene libro: añadirlo a `data/libros.json` y
      regenerar (`build_pages`) + `sync_video_descriptions.py --add-books --channel club`

## Prioridad 1: las 3 ventas de Amazon (tag `senalabierta-21`)

- [ ] Mención verbal del libro en los próximos 5 vídeos del Club
      (guión de 10 s al final: "el libro de esta historia está enlazado
      abajo y en el hub")
- [ ] Comentario fijado con el enlace del libro en los vídeos con libro
      mapeado (link con `utm_medium=pinned_comment`)
- [ ] Primer digest: libro de la semana destacado (el script ya lo hace)
- [ ] Semanal: Central de Afiliados → informes → pedidos;
      **al llegar a 3 ventas → pedir revisión del sitio**
      (plazo del programa: 180 días desde el alta)
- Plan B (día 60 sin ventas): banner en `/libros/` + mención fija

## Ko-fi

- [ ] Intro del perfil y 3 enlaces (hub, canal, newsletter)
- [x] Hecho: enlace en footer del hub + en las 94 descripciones
- [ ] Webhook activo: `https://senalabierta.pages.dev/api/kofi` en
      Ko-fi → Webhooks → Send a test (token en env-var `KOFI_TOKEN`,
      pagos en KV con prefijo `kofi:`)

## Medición (cada lunes)

- [x] **Tablero unico**: `python scripts/monetization.py` → visitas,
      suscriptores, aperturas, donaciones Ko-fi y smoke en un solo comando
- [ ] Visitas del hub: `GET https://senalabierta.pages.dev/api/stats`
      (contador propio: total, últimos 30 días y rutas top)
- [ ] YouTube Analytics → Alcance → Fuentes externas: `senalabierta.pages.dev`
- [ ] Buttondown → suscriptores y open rate
- [ ] Amazon Central de Afiliados → clics, carritos, pedidos
- [ ] Pendientes de alta: Quipu, ElevenLabs, NordVPN (`TODO-AFILIADO`)

## Infra (una vez)

- [x] `.env` con `BUTTONDOWN_API_KEY` (plantilla en `.env.example`)
- [ ] Cobro: PayPal (o Stripe) conectado en Ko-fi → Payment Settings;
      Amazon/NordVPN/ElevenLabs pagan por su propio canal (IBAN o PayPal
      configurado en cada plataforma, no se conecta al hub)
- [ ] Google Search Console: propiedad + sitemap (102 URLs)
- [ ] QA visual del hub, `/libros/` y landings (capturas en pantalla)
