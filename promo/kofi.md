# Ko-fi — pack para empezar a ganar

Estado (2026-10-02): PayPal conectado ✅ · webhook `/api/kofi` verificado ✅ ·
bio base ✅ · **PRODUCTO PUBLICADO ✅ → https://ko-fi.com/s/c7fd921388**
(5 USD PWYW · thumbnail `portada-kofi.png` · preview = Tip #50
`youtube.com/watch?v=2uDS8sIbM9o`). FALTAN:
avatar, 3 enlaces, categorías, tiers de membresía y promoción del enlace.
Este fichero tiene todo listo para pegar.

> **Ko-fi no tiene API pública**: nada de esto se puede automatizar desde
> aquí — son 10-15 min manuales en ko-fi.com con este fichero al lado.

## 1. Tu página (ko-fi.com → "Your page") — 5 min

- **Avatar**: sube logo o foto (ahora sale la imagen genérica gris).
- **Categorías**: ahora pone "Animation Software Writing Video and Film Money"
  (categorías por defecto) → cámbialas por **Business, Technology, Education**.
- **Tus 3 enlaces** (botón de enlaces del perfil):
  1. Hub: `https://senalabierta.pages.dev/?utm_source=kofi&utm_medium=profile&utm_campaign=senal_abierta`
  2. Canal: `https://www.youtube.com/@historiasdenegocios-o5m`
  3. Newsletter: `https://buttondown.com/revolvere`
- **Bio (opcional, versión con CTA)**:

  > Historias de negocios e IA, sin ruido. Cada semana, vídeos nuevos y el
  > archivo completo en senalabierta.pages.dev. Si te aporta algo,
  > invítame a un café ☕

- **Goal** (opcional): "Primeros 100 € para producir mejor el canal".

## 2. Membresías (menú Memberships → Set up your membership tiers)

Ingreso recurrente. Ko-fi cobra 5% (tips: 0%). Precios pensados para ES:

| Tier | Precio/mes | Beneficios (texto listo para pegar) |
|------|-----------|--------------------------------------|
| **Café** | 3 € | "Gracias por apoyar el canal ☕. Acceso a mis posts exclusivos: detrás de cámaras, qué estoy probando y resúmenes antes que nadie." |
| **Socio** | 7 € | "Todo lo del tier Café + **votas el siguiente libro/tema** de El Club del Negocio y apareces en los agradecimientos del hub." |
| **Patrón** | 15 € | "Todo lo anterior + mención en la página de créditos del hub + una sesión mensual de preguntas en directo." |

Reglas: si activas tiers, publica **1 post/mes mínimo** en el feed de Ko-fi
(exclusivo para socios) — es lo que retiene la membresía.

## 3. Shop — producto 1 listo para subir

**Generado (2026-10-01):** `promo/productos/30-prompts/30-prompts-senal-abierta.pdf`
(14 páginas · 30 prompts reales de los tips del canal + 3 recetas bonus).
Fuente editable: `contenido_a.py` / `contenido_b.py` → regenerar con
`python build_pdf.py`.

Pasos en Ko-fi (ko-fi.com → Shop → Add shop item → Digital product):

1. **Name**: `30 prompts de IA para trabajar el doble en la mitad de tiempo`
2. **Price**: `5` (€, si Ko-fi te deja elegir divisa; si no, `5 USD` — ~4,6 €)
3. **Description** (pegar tal cual):

   > Los prompts exactos de los tips de Señal Abierta, listos para copiar y
   > pegar. 30 prompts en 9 bloques: productividad, tareas programadas,
   > investigación, carrera, copy, tu voz para newsletters, imágenes y
   > miniaturas, presentaciones y código. Cada uno con variables listas,
   > cuándo usarlo y un truco de aprovechamiento. Bonus: 3 recetas de vídeo
   > (Gemini, Suno, Veo 3). Enlaces directos a cada vídeo original del canal.
   > Uso personal: cópialos, mézclalos, adáptalos.

4. **Tags**: `prompts`, `ia`, `chatgpt`, `productividad`
5. **Upload file**: el PDF de arriba.
6. **Thumbnail**: usa `promo/productos/30-prompts/portada-kofi.png`
   (1200×900; fondo generado con IA — Flux vía NIM / Z-Image local — y
   texto compuesto con `python build_portada.py`).

Siguientes productos (cuando pidas): plantilla 50/30/20 (3 €), ebook de
historias de negocios (7 €).

## 4. Dónde promocionar (lo que de verdad trae los primeros euros)

- [ ] **Banner de ambos canales** → enlace Ko-fi con UTM
      (`promo.md` § links: `utm_medium=banner`).
- [ ] **Comentario fijado** en los últimos 3-5 vídeos (plantilla `promo.md` §4).
- [ ] Bio de **X / TikTok / Instagram / Threads** (§5).
- [ ] Ya activo sin hacer nada: enlace en las **98 descripciones**,
      footers del hub/landings/libros y en la newsletter.
- [ ] Mención verbal: "si os sirvió, invítame a un café" en los
      próximos 5 vídeos del Club.

## 5. Cómo llega el dinero (ya configurado)

```
Fan pulsa el enlace → paga con PayPal/tarjeta → entra en TU PayPal
         └→ Ko-fi hace POST /api/kofi → queda registrado en KV
            (ver con: python scripts/monetization.py)
```

- Tips: Ko-fi **0%** (solo comisión de tu pasarela, PayPal ≈1,74%+0,34 €).
- Membresías/Shop: Ko-fi 5% (o 0% con Ko-fi Gold, 12 $/mes — solo merece
  la pena a partir de ≈240 $/mes de ventas).

## 6. Expectativa honesta

Con ~3.700 views/mes: tips realistas los primeros meses = **0-10 €/mes**.
El multiplicador es tráfico (banner + fijados + GSC) y, sobre todo,
convencer a 1-3 socios mensuales (3-21 €/mes recurrentes). Sube exponencial
si crece el canal.
