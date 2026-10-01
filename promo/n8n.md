# n8n en Señal Abierta — workflow de Ko-fi

Estado (2026-10-01): n8n **instalado** en este PC (`n8n` en PATH + `~/.n8n`),
workflow listo en `promo/n8n/kofi-workflow.json`. Falta montarlo en la UI
(5 min) y, opcional, conectar Google Sheets/Gmail.

## Por qué polling y no webhook directo

- Ko-fi permite **un solo webhook** y ya apunta a
  `https://senalabierta.pages.dev/api/kofi` (Pages Functions + KV), que está
  siempre en pie y alimenta el dashboard y `python scripts/monetization.py`.
- Tu n8n es **local** (tu PC): Ko-fi no puede alcanzarlo desde internet sin
  túncel/tunnel, y si el PC se apaga se pierden eventos.
- Diseño elegido: **n8n consulta** `GET /api/kofi?limit=100` cada 3 h,
  detecta pagos nuevos por `id` y ejecuta acciones. Sin túneles, sin perder
  el registro central.

```
Ko-fi ──POST──▶ senalabierta.pages.dev/api/kofi ──▶ KV (fuente de verdad)
                                                        ▲
n8n (cada 3h) ──GET /api/kofi?limit=100──filtrar nuevos─┘
        └─▶ Google Sheets / Gmail / Discord (lo que conectes)
```

## Montaje (5 min)

1. Abre la UI de n8n: `n8n start` (o `npm exec -- n8n start`) y entra en
   http://localhost:5678
2. **Workflows → Import from File** → selecciona `promo/n8n/kofi-workflow.json`
3. El nodo **Fila en Google Sheets** viene **deshabilitado** con marcadores
   `PEGA_AQUI_...`. Para activarlo:
   - Crea una Sheet con columnas: `fecha, tipo, importe, moneda, de, mensaje`
   - En n8n: credencial Google Sheets OAuth2 → pega el ID del documento
   - Quita el *disabled* al nodo
4. (Opcional) Añade tras el nodo de filtro un **Gmail → Send email** para
   agradecer cada donación: asunto `Gracias por el café, {{ $json.from }}`,
   cuerpo 3 líneas + enlace al canal.
5. **Activate** (interruptor arriba a la derecha).

La **primera ejecución siembra** sin notificar (no agradece los pagos
históricos); a partir de ahí solo procesa los nuevos.

## Ideas siguientes (cuando quieras)

- **Digest semanal del lunes**: Schedule (lun 9:00) → HTTP
  `python scripts/newsletter_draft.py --apply` vía Execute Command →
  PATCH Buttondown `about_to_send` → newsletter enviada sin tocar nada.
- **Agradecimiento proactivo** de socios de membresía (mismo patrón de poll).
- **Discord/Telegram**: nodo de aviso rápido en vez de Sheets.

## Comandos útiles

```powershell
# arrancar n8n
n8n start

# ver lo que hay ahora mismo en KV (pagos registrados)
python scripts/monetization.py

# comprobar el endpoint que consume n8n
curl https://senalabierta.pages.dev/api/kofi?limit=5
```
