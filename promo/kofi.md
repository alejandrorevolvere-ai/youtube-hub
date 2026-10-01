# Ko-fi — pack para empezar a ganar

Estado (2026-10-01): PayPal conectado ✅ · webhook `/api/kofi` verificado ✅ ·
bio base ✅. FALTAN: avatar, 3 enlaces, categorías, tiers de membresía y
promoción del enlace. Este fichero tiene todo listo para pegar.

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

## 3. Shop (futuro — segundo paso)

Productos digitales que puedo generarte (pides uno y lo monto):
1. **Pack de 30 prompts de IA** del canal IA en 60 segundos (PDF, 5 €).
2. **Plantilla 50/30/20 + hoja de cálculo** de ahorro (3 €).
3. **Ebook**: "Las 20 historias de negocios mejor contadas" (del archivo, 7 €).

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
