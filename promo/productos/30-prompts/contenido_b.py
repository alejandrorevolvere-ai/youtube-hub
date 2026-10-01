# -*- coding: utf-8 -*-
"""Contenido del pack: secciones 5-9 + recetas bonus."""
from links import link

SECTIONS_B = [
    {
        "title": "Copy que convierte",
        "intro": "Un prompt, diez variantes: headlines, emails, anuncios y guion de venta.",
        "prompts": [
            {
                "title": "Copywriter direct-response completo",
                "tool": "ChatGPT",
                "source": "Prompt único: Copy que convierte (Tip #44)",
                "url": link("prompt-unico-copy-que-convierte-copia-y-pega-tip-44"),
                "when": "Lanzamiento de producto, campaña o landing nueva.",
                "text": "Actúa como copywriter senior direct-response. "
                        "Producto: [PRODUCTO]. Avatar: [AVATAR]. Dolor: [DOLOR]. Deseo: [DESEO]. "
                        "Entrega: 1) 5 headlines gancho (curiosidad + beneficio), "
                        "2) 3 emails de secuencia (gancho -> historia -> oferta), "
                        "3) 2 anuncios para Facebook/IG (texto principal + headline), "
                        "4) 1 guion de vídeo de venta de 60 segundos. "
                        "Formato: listo para publicar, sin meta-comentarios.",
                "vars": "[PRODUCTO] = tu oferta. [AVATAR] = quién compra. [DOLOR] = qué le quita el sueño. [DESEO] = qué quiere de verdad.",
                "truco": "Si sale demasiado infomercial, añade al final: 'tono conversacional, sin hype'.",
            },
            {
                "title": "Fórmula de prompts comerciales (rol + gatillos + CTA)",
                "tool": "ChatGPT",
                "source": "Fórmula de prompts comerciales del canal",
                "url": None,
                "when": "Cuando necesites copy de venta rápido para redes o anuncios.",
                "text": "Actúa como un vendedor experto con 20 años vendiendo [TIPO DE PRODUCTO]. "
                        "Producto objetivo: [PRODUCTO]. Cliente ideal: [CLIENTE]. "
                        "Escribe un copy que use gatillos mentales honestos: prueba social, escasez real "
                        "y un llamado a la acción directo. "
                        "Entrega: 1) 3 titulares, 2) párrafo de venta de 80 palabras, 3) CTA final. "
                        "Sin promesas que no se puedan cumplir.",
                "vars": "[TIPO DE PRODUCTO], [PRODUCTO], [CLIENTE] = lo que vendas, incluso si es un servicio freelance.",
                "truco": "Pide '3 variaciones del CTA' y quédate con la que diga lo mismo con menos palabras.",
            },
        ],
    },
    {
        "title": "Tu voz, tus newsletters",
        "intro": "La IA escribe como tú (no como la IA): primero le enseñas tu voz.",
        "prompts": [
            {
                "title": "Voice profile (extrae tu voz en JSON)",
                "tool": "ChatGPT",
                "source": "Escribí 50 newsletters en 2h con este sistema (Tip #19)",
                "url": link("escribi-50-newsletters-en-2h-con-este-sistema-tip-19"),
                "when": "Una vez por cada cambio importante de estilo. Guarda el resultado.",
                "text": "Analiza estos 5 textos míos: [PEGA 5 NEWSLETTERS O TEXTOS]. "
                        "Extrae: tono, longitud media de frase, vocabulario favorito, "
                        "estructura de párrafos y nivel de humor. "
                        "Entrega JSON con las claves: tone, sentence_length, vocabulary, structure, humor. "
                        "Y después, en 3 frases en lenguaje llano, qué hace único mi estilo.",
                "vars": "[PEGA 5 TEXTOS] = cosas que YA escribiste tú (no textos de la IA).",
                "truco": "Guarda el JSON como voice.json: es el motor de todo el sistema de newsletters.",
            },
            {
                "title": "Newsletter en tu voz con tus fuentes",
                "tool": "ChatGPT",
                "source": "Escribí 50 newsletters en 2h con este sistema (Tip #19)",
                "url": link("escribi-50-newsletters-en-2h-con-este-sistema-tip-19"),
                "when": "Fase 2 del sistema, con las fuentes ya curadas.",
                "text": "Voice: [PEGA voice.json O LAS 3 FRASES DE TU ESTILO]. "
                        "Fuentes: [PEGA LA TABLA DE 10 FUENTES]. "
                        "Escribe la newsletter: hook de 1 frase -> 3 insights -> 1 consejo accionable -> CTA. "
                        "400 palabras, mi voz, sin relleno, sin frases de manual.",
                "vars": "[TABLA DE FUENTES] = la salida del prompt de curación de fuentes.",
                "truco": "Si suena a IA, añade al final: 'reescribe con más personales y menos adverbios'.",
            },
        ],
    },
    {
        "title": "Imágenes y miniaturas",
        "intro": "Seis plantillas para Ideogram (texto impecable) o Midjourney (acabado de cine).",
        "prompts": [
            {
                "title": "Miniatura con texto (el rey: Ideogram)",
                "tool": "Ideogram",
                "source": "La verdad incómoda sobre la IA que dibuja (Tip #29)",
                "url": link("la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29"),
                "when": "Miniaturas de YouTube con título encima: aquí Midjourney deforma las letras.",
                "text": "Miniatura de YouTube 16:9. Sujeto: [SUJETO], primer plano, iluminación dramática. "
                        "Texto grande y legible en la parte superior: \"[TEXTO DE LA MINIATURA]\", "
                        "tipografía sans-serif bold, alto contraste. "
                        "Fondo con espacio negativo a la derecha. Sin marcos de agua. "
                        "Estilo: vibrante, colores saturados.",
                "vars": "[SUJETO] = lo que aparece. [TEXTO] = máx. 4 palabras (p.ej. 'IA TE REEMPLAZA').",
                "truco": "Ideogram escribe bien el texto; Midjourney gana en arte. Para miniaturas con palabras, no lo dudes.",
            },
            {
                "title": "Retrato cinematográfico",
                "tool": "Midjourney",
                "source": "La verdad incómoda sobre la IA que dibuja (Tip #29)",
                "url": link("la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29"),
                "when": "Avatares, portadas de personas, imágenes de artículo.",
                "text": "Retrato cinematográfico de [PERSONA/DESCRIPCIÓN], piel texturizada, "
                        "mirada a cámara, luz de contraclave naranja y azul, "
                        "profundidad de campo corta, objetivo 85mm, render fotorrealista --ar 4:5 --style raw",
                "vars": "[PERSONA/DESCRIPCIÓN] = p.ej. 'una mujer ingeniera de 30 años en un laboratorio'.",
                "truco": "--style raw quita el embellecimiento por defecto: los rasgos se mantienen fieles.",
            },
            {
                "title": "Paisaje de fondo",
                "tool": "Midjourney / Ideogram",
                "source": "La verdad incómoda sobre la IA que dibuja (Tip #29)",
                "url": link("la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29"),
                "when": "Fondos para presentaciones, vídeos o posts.",
                "text": "Paisaje de [LUGAR IMAGINARIO], hora dorada, niebla baja entre las montañas, "
                        "composición en capas, colores teal y ámbar, estilo matte painting de película, "
                        "detalle alto, sin personas, sin texto --ar 16:9",
                "vars": "[LUGAR IMAGINARIO] = p.ej. 'valle volcánico al amanecer'.",
                "truco": "Añade 'sin personas y sin texto' cuando quieras fondo limpio para superponer títulos.",
            },
            {
                "title": "Logo con texto legible",
                "tool": "Ideogram",
                "source": "La verdad incómoda sobre la IA que dibuja (Tip #29)",
                "url": link("la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29"),
                "when": "Bocetos de marca (luego un diseñador lo termina).",
                "text": "Logotipo minimalista para [TIPO DE NEGOCIO], símbolo [SÍMBOLO O IDEA], "
                        "tipografía geométrica sans-serif, nombre exacto del negocio: \"[NOMBRE]\", "
                        "fondo blanco, colores [2 COLORES], vectores limpios, sin degradados, sin sombras --ar 1:1",
                "vars": "[NOMBRE] = escríbelo exacto, letra por letra: es donde las IA fallan.",
                "truco": "Genera 4 variantes y elige la que leas bien a tamaño de favicon.",
            },
            {
                "title": "Estilo anime",
                "tool": "Midjourney",
                "source": "La verdad incómoda sobre la IA que dibuja (Tip #29)",
                "url": link("la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29"),
                "when": "Ilustraciones de personajes, posteos creativos, arte de canal.",
                "text": "Ilustración anime estilo [SHONEN/SLICE-OF-LIFE/CIBERPUNK] de [ESCENA], "
                        "expresión [EMOCIÓN], cabello al viento, fondo bokeh de [LUGAR], "
                        "líneas limpias, colores vivos, iluminación suave de contraluz, alta calidad --ar 3:4",
                "vars": "[SHONEN/...] = el subgénero. [ESCENA] = la acción concreta.",
                "truco": "Para un personaje recurrente del canal, guarda su descripción física y répítela en cada prompt.",
            },
            {
                "title": "Fotorealismo de producto",
                "tool": "Midjourney",
                "source": "La verdad incómoda sobre la IA que dibuja (Tip #29)",
                "url": link("la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29"),
                "when": "Mockups de producto, imágenes de post o landing sin sesion de fotos.",
                "text": "Fotografía de producto: [PRODUCTO] sobre [SUPERFICIE], "
                        "luz de estudio suave desde la izquierda, sombra natural, "
                        "reflejos controlados, fondo limpio [COLOR], detalle macro, "
                        "aspecto premium, sin texto, sin logos de terceros --ar 4:3 --style raw",
                "vars": "[PRODUCTO] = p.ej. 'auriculares inalámbricos blancos'. [SUPERFICIE] = 'una mesa de mármol'.",
                "truco": "Midjourney brilla en fotorealismo: aquí no compites con Ideogram, compites con un estudio.",
            },
        ],
    },
    {
        "title": "Presentaciones y reuniones",
        "intro": "Del documento de 20 páginas a slides para mañana; de la reunión a tareas sin teclado.",
        "prompts": [
            {
                "title": "Doc entero a presentación (Gamma)",
                "tool": "Gamma",
                "source": "Convierte cualquier doc en presentación (Tip #39)",
                "url": link("convierte-cualquier-doc-en-presentacion-prompt-gamma-tip-39"),
                "when": "Tienes el informe y la reunión es mañana.",
                "text": "Transforma este documento en presentación de [N] slides para [AUDIENCIA]. "
                        "Estructura: 1) hook (problema + promesa), 2-3) contexto clave solo accionable, "
                        "4-8) solución o insights (1 idea por slide, con apoyo visual), "
                        "9) prueba o caso real, 10) próximos pasos + CTA. "
                        "Estilo: [MINIMALISTA/CORPORATIVO/CREATIVO]. Elimina relleno. "
                        "Máximo 40 palabras por slide. Incluye notas del orador por slide.",
                "vars": "[N] = 8-12. [AUDIENCIA] = inversores / equipo / clientes. [ESTILO] = según tu marca.",
                "truco": "Pega el doc completo dentro del prompt (o adjúntalo): la calidad del slide sale de ahí.",
            },
            {
                "title": "Project brief automático",
                "tool": "Notion IA",
                "source": "3 templates Notion IA que uso diario",
                "url": link("3-templates-notion-ia-que-uso-diario-duplica-y-listo"),
                "when": "Al abrir cualquier proyecto nuevo en Notion.",
                "text": "Contexto de este proyecto: [PÁGINA DEL PROYECTO]. "
                        "Escribe el brief: objetivo, alcance (qué es y qué NO es), stakeholders, "
                        "riesgos, timeline y definition of done. "
                        "Formato: las 6 secciones con viñetas, máximo 15 líneas en total.",
                "vars": "[PÁGINA DEL PROYECTO] = enlázala o pega sus notas sueltas.",
                "truco": "La sección 'qué NO es' es la que evita el scope creep: no la quites nunca.",
            },
            {
                "title": "Reunión a tareas en JSON (Fireflies)",
                "tool": "Fireflies · Custom App",
                "source": "Prompt Fireflies: de transcripción a tasks en Notion",
                "url": link("prompt-fireflies-de-transcripcion-a-tasks-en-notion-auto"),
                "when": "Una vez configurado, corre solo tras cada reunión.",
                "text": "Analiza esta reunión. Entrega JSON estricto con: decisions, "
                        "action_items (con responsable y fecha límite), blockers y followups. "
                        "Solo incluye lo dicho explícitamente; no infieras. "
                        "Si no hay nada en una categoría, devuelve la lista vacía.",
                "vars": "Configúralo en Fireflies > AI Apps > Custom App > auto-run tras la llamada; conecta el webhook a Notion.",
                "truco": "Añade el campo related_project para auto-enlazar con tu base de proyectos en Notion.",
            },
            {
                "title": "Resumen ejecutivo de 3 bullets (para Slack)",
                "tool": "ChatGPT / Notion IA",
                "source": "3 templates Notion IA que uso diario",
                "url": link("3-templates-notion-ia-que-uso-diario-duplica-y-listo"),
                "when": "Cuando necesites avisar al equipo sin escribir el aviso.",
                "text": "Resume esto en 3 bullets para Slack, para alguien que no ha leído nada de lo anterior: "
                        "[PEGA EL TEXTO O LA TRANSCRIPCIÓN]. "
                        "Cada bullet: qué pasó -> qué implica -> qué se espera de quien lo lea. "
                        "Sin saludo, sin cierre, sin emojis.",
                "vars": "[PEGA] = informe, transcripción o hilo largo.",
                "truco": "Si algún bullet supera las 12 palabras, no es un bullet: pídelo más corto.",
            },
        ],
    },
    {
        "title": "Código con contexto (nivel senior)",
        "intro": "La diferencia entre novato y senior no es el modelo: es el contexto que le das.",
        "prompts": [
            {
                "title": "Generador con contexto completo (service + tests + migración)",
                "tool": "ChatGPT / Claude / Copilot",
                "source": "Cómo usan ChatGPT los devs senior (Tip #14)",
                "url": link("como-usan-chatgpt-los-devs-senior-vs-novatos-tip-14"),
                "when": "Feature nueva en un repo existente: el output sale listo para merge.",
                "text": "Repo: [ESTRUCTURA DEL REPO]. Patterns: repository + service. "
                        "Convenciones: types estrictos, docstrings estilo Google. "
                        "Edge cases a cubrir: rate limit, idempotencia. "
                        "Genera: [FEATURE], con tests y migración si toca. "
                        "Asume que el código pasa el linter del repo sin tocar su configuración.",
                "vars": "[ESTRUCTURA DEL REPO] = árbol de carpetas + 1-2 ejemplos de módulos ya existentes.",
                "truco": "Nivel 1: 'hazme una API' da código genérico. Nivel 2: añades el stack y quedan decisiones implícitas. "
                        "Este es el nivel 3: contexto completo, ahorra 2-4h por feature.",
            },
        ],
    },
]

RECETAS = [
    {
        "title": "Receta con foto de tu nevera (Gemini)",
        "source": "Gemini cocina con lo de TU nevera (Tip #73)",
        "url": link("gemini-cocina-con-lo-de-tu-nevera-solo-con-una-foto-tip-73"),
        "steps": "Foto de la nevera -> Gemini la adjunta -> pide: 'Con lo que ves, dame 3 recetas, "
                 "cuánto tarda cada una y qué ingredientes me faltan'. Funciona también con armarios, "
                 "facturas en otro idioma o cualquier cosa fotografiada.",
    },
    {
        "title": "Canción en 2 minutos (Suno)",
        "source": "Hice una CANCION con IA (Tip #72)",
        "url": link("hice-una-cancion-con-ia-en-2-minutos-escucha-esto-tip-72"),
        "steps": "Describe estilo + escribe la letra (o pide que la invente) -> genera -> descarga. "
                 "Plan gratis con créditos diarios. Sirve para regalos, tu negocio o tu primer single.",
    },
    {
        "title": "Fondos y b-roll gratis (Veo 3 en Shorts)",
        "source": "Veo 3 genera video CON sonido (Tip #45)",
        "url": link("nuevo-veo-3-genera-video-con-sonido-gratis-en-shorts-tip-45"),
        "steps": "En la app de YouTube: Crear -> Efectos -> IA. Describe la escena "
                 "(p.ej. 'oficina futurista de noche') y genera el clip con sonido en segundos. "
                 "Perfecto para fondos y hooks de 3 segundos; se etiqueta como contenido IA.",
    },
]
