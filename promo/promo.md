# Textos de promoción — listos para pegar

Todo usa el hub como puerta de entrada. Los enlaces llevan UTM por plataforma
(`utm_source`) para que en YouTube Analytics el tráfico externo sea
identificable y las URLs queden diferenciadas.

**URL base del hub:** `https://senalabierta.pages.dev/`

> Nota: YouTube Analytics mide el tráfico externo por el dominio de referencia
> (ya activo: `strict-origin-when-cross-origin`). Los UTM identifican cada
> enlace de forma única; el hub tiene Cloudflare Web Analytics (sin cookies),
> donde los UTM de entrada quedan recolectados para ver el tráfico inverso
> (Google → hub → YouTube).

---

## 1. Enlaces con UTM por plataforma (copiar y pegar)

| Dónde va | URL con UTM |
|---|---|
| Bio X | `https://senalabierta.pages.dev/?utm_source=x&utm_medium=bio&utm_campaign=senal_abierta` |
| Bio TikTok | `https://senalabierta.pages.dev/?utm_source=tiktok&utm_medium=bio&utm_campaign=senal_abierta` |
| Bio Instagram | `https://senalabierta.pages.dev/?utm_source=instagram&utm_medium=bio&utm_campaign=senal_abierta` |
| Bio Threads | `https://senalabierta.pages.dev/?utm_source=threads&utm_medium=bio&utm_campaign=senal_abierta` |
| Descripción (About) del canal | `https://senalabierta.pages.dev/?utm_source=youtube&utm_medium=channel_about&utm_campaign=senal_abierta` |
| Comentario fijado en vídeos | `https://senalabierta.pages.dev/?utm_source=youtube&utm_medium=pinned_comment&utm_campaign=senal_abierta` |
| Newsletter / mailing | `https://senalabierta.pages.dev/?utm_source=newsletter&utm_medium=email&utm_campaign=senal_abierta` |
| CTA descripciones de YouTube | `https://senalabierta.pages.dev/v/{slug}/?utm_source=youtube&utm_medium=description&utm_campaign=senal_abierta` |
| Pie de landings (newsletter) | `https://buttondown.com/revolvere?utm_source=senalabierta&utm_medium=newsletter&utm_campaign=landing` |
| CTA hub (botón newsletter) | `https://buttondown.com/revolvere?utm_source=senalabierta&utm_medium=newsletter&utm_campaign=hub` |
| Ko-fi (footer/descripciones) | `https://ko-fi.com/alejandrorevolvere?utm_source=senalabierta&utm_medium=kofi&utm_campaign=senal_abierta` |
| Libros (`/libros/` y descripciones) | `https://www.amazon.es/dp/{ASIN}?tag=senalabierta-21&utm_source=senalabierta&utm_medium=affiliate&utm_campaign=libros` |
| Firma de foro / Discord | `https://senalabierta.pages.dev/?utm_source=foro&utm_medium=firma&utm_campaign=senal_abierta` |
| Firma de email | `https://senalabierta.pages.dev/?utm_source=email&utm_medium=firma&utm_campaign=senal_abierta` |

---

## 2. Descripción (Acerca de) — canal El Club del Negocio

```
Historias de empresas, el dinero detrás de cada decisión y lecciones que convierten una idea en movimiento.

🆕 Todo el archivo ordenado en un solo sitio: https://senalabierta.pages.dev/?utm_source=youtube&utm_medium=channel_about&utm_campaign=senal_abierta

Nuevo vídeo cada semana. Suscríbete y activa la campana 🔔
```

## 3. Descripción (Acerca de) — canal IA en 60 segundos

```
Una idea poderosa de IA explicada en el tiempo que tardas en decidir: herramientas gratis, flujos y atajos reales.

🆕 Nuevo cada semana + todos los vídeos aquí: https://senalabierta.pages.dev/?utm_source=youtube&utm_medium=channel_about&utm_campaign=senal_abierta

Suscríbete 🔔
```

---

## 4. Comentario fijado (plantilla — pegar en cada vídeo nuevo)

```
👉 ¿Esto te sirvió? En el hub tienes el resto del archivo, ordenado por canal:
https://senalabierta.pages.dev/?utm_source=youtube&utm_medium=pinned_comment&utm_campaign=senal_abierta

¿De qué tema quieres el próximo vídeo? Déjalo en un comentario 👇
```

---

## 5. Bios por red social

### X (Twitter) — límite 160
```
Negocios, dinero e IA en vídeos de 60". Dos canales, una señal. 👉 youtube-hub
```
*(pegar con la URL de la tabla: la bio de X solo admite 160 caracteres, usa la URL corta `https://senalabierta.pages.dev/` directamente)*

### TikTok — límite 80
```
IA y negocio en 60". Los 2 canales aquí ⬇️
```

### Instagram — límite 150
```
Vídeos breves de negocio e IA. Los DOS canales, un solo sitio ⬇️ (link en bio)
```

### Threads — límite ~50
```
Negocio + IA en 60". Dos canales →
```

---

## 6. Textos para compartir en foros / Discord / newsletters

**Corto (2-3 líneas):**
```
Lancé "Señal Abierta", un hub con mis dos canales: historias de negocio e
inteligencia artificial en vídeos de un minuto. Todo el archivo en un solo
lugar: https://senalabierta.pages.dev/?utm_source=foro&utm_medium=firma&utm_campaign=senal_abierta
```

**Medium (para Discord/newsletter):**
```
Señal Abierta — ideas que mueven decisiones.

Dos canales, una señal:
• El Club del Negocio: historias de empresas y el dinero detrás de cada decisión
• IA en 60": una idea de IA explicada en el tiempo que tardas en decidir

Vídeos breves, sin humo. Aquí está todo el archivo ordenado:
https://senalabierta.pages.dev/?utm_source=newsletter&utm_medium=email&utm_campaign=senal_abierta
```

---

## 7. Checklist de promoción

- [ ] **URL nueva** (`https://senalabierta.pages.dev/`): reemplazar la antigua
      `alejandrorevolvere-ai.github.io/youtube-hub/` en bios, links de banner y
      comentarios fijados ya publicados (la URL vieja redirige, pero conviene
      actualizarla)
- [ ] Enlace del hub en los Links del banner de **ambos canales** (Customizar canal → Vínculos)
- [ ] Descripción actualizada (secciones 2 y 3) en ambos canales
- [ ] Comentario fijado (sección 4) en los últimos 3-5 vídeos
- [ ] Bio + link en X, TikTok, Instagram y Threads (sección 5)
- [ ] Firma en Discord/foros habituales (sección 6)
- [ ] Compartir la sección `#senal` del hub al salir un vídeo nuevo
- [ ] Revisar en YouTube Analytics → Alcance → Fuentes de tráfico → Externo
      (debería aparecer `senalabierta.pages.dev` como fuente)
