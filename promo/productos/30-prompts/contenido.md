# 30 prompts de IA — Señal Abierta (fuente editable)

Regenerar el PDF: `python build_pdf.py`

## Productividad y organización
_Menos gestión, más resultado. Estos 6 prompts cubren la semana completa de trabajo._

### 1. Planificador semanal (chief of staff)
- Herramienta: ChatGPT — [3 prompts que me ahorran 10h/semana (Tip #50)](https://senalabierta.pages.dev/v/3-prompts-de-chatgpt-que-me-ahorran-10h-semana-tip-50/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Los domingos por la noche o los lunes a primera hora.
- Variables: [METAS] = tus 2-3 objetivos. [HORAS LIBRES] = huecos reales de tu semana.
- Truco: Pega la lista de tareas que ya tengas: el plan sale realista en el primer intento.

```
Actúa como mi chief of staff. Aquí están mis metas del mes: [METAS]. Mi disponibilidad es [HORAS LIBRES]. Genera un plan día por día de esta semana con bloques de 90 minutos, priorizando lo que más acerca mis metas. Marca 1 bloque de foco profundo al día y 1 margen para imprevistos. Formato: tabla (día | bloque | tarea | resultado esperado).
```

### 2. Procesador de emails (suena a ti)
- Herramienta: ChatGPT — [3 prompts que me ahorran 10h/semana (Tip #50)](https://senalabierta.pages.dev/v/3-prompts-de-chatgpt-que-me-ahorran-10h-semana-tip-50/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Cuando tengas 10+ emails pendientes: pega los 10 de golpe.
- Variables: [CONTEXTO] = 'cliente', 'jefe', 'proveedor'... [PEGA EMAILS] = numerados (1., 2., 3.).
- Truco: Revisa y ajusta antes de enviar: el 90% sirve tal cual, el 10% final lo personalizas tú.

```
Responde cada email como yo. Mi relación con el remitente: [CONTEXTO]. Tono: directo, empático, con acción clara. Máximo 3 líneas por respuesta. Sin relleno, sin disculpas inventadas, sin prometer lo que no puedo cumplir.

Emails:
[PEGA EMAILS]
```

### 3. Resumen de reuniones (decisiones + tareas)
- Herramienta: ChatGPT / Notion IA — [3 prompts que me ahorran 10h/semana (Tip #50)](https://senalabierta.pages.dev/v/3-prompts-de-chatgpt-que-me-ahorran-10h-semana-tip-50/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: En cuanto termine cualquier reunión con transcripción.
- Variables: [PEGA TRANSCRIPCIÓN] = la de Zoom/Meet/Teams/Fireflies.
- Truco: Añade 'y una frase: ¿quedó claro el siguiente paso?' para detectar reuniones mal cerradas.

```
Transcripción: [PEGA TRANSCRIPCIÓN]. Extrae: 1) 3 decisiones tomadas, 2) 5 action items con responsable y fecha, 3) riesgos o bloqueos abiertos. Solo lo que aparece explícito en la transcripción; no infieras ni rellenes huecos. Formato: tres tablas separadas.
```

### 4. Inbox a cero (segundo cerebro)
- Herramienta: Notion IA — [Mi segundo cerebro en Notion IA (Tip #66)](https://senalabierta.pages.dev/v/mi-segundo-cerebro-en-notion-ia-captura-organiza-acciona-tip-66/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Cada noche, con tu base Inbox de Notion.
- Variables: Sin variables: funciona directo sobre tu base Inbox.
- Truco: Si tu Inbox supera los 30 items, ejecútalo dos noches seguidas hasta dejarlo limpio.

```
Revisa la base Inbox. Mueve cada item a su proyecto o área. Crea tareas con fecha para todo lo accionable. Resume en una línea los items que requieran más de 5 minutos de lectura. Responde solo con la lista de cambios realizados.
```

### 5. Plan del día con tus reuniones
- Herramienta: Notion IA — [3 templates Notion IA que uso diario](https://senalabierta.pages.dev/v/3-templates-notion-ia-que-uso-diario-duplica-y-listo/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Botón 'Plan IA' en tu Daily Planner, cada mañana.
- Variables: Sin variables: conecta el botón a tu calendario y base de tareas.
- Truco: Regla de las 3 prioridades: si el día solo dejara tiempo para 3 cosas, ¿cuáles serían?

```
Lee mis reuniones de hoy y mis tareas abiertas. Genera: 3 prioridades del día, bloques de tiempo y margen de buffer entre reuniones. Formato: horario del día, de la primera reunión a la última.
```

### 6. Action items desde transcripción (a tu base Tasks)
- Herramienta: Notion IA — [3 templates Notion IA que uso diario](https://senalabierta.pages.dev/v/3-templates-notion-ia-que-uso-diario-duplica-y-listo/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Botón 'Action items' sobre cualquier reunión transcrita.
- Variables: [PROPIEDAD DE LA REUNIÓN] = el texto de la transcripción pegado en la página.
- Truco: Añade 'relaciona cada tarea con su proyecto' para mantener tu tabla Projects viva.

```
Transcripción: [PROPIEDAD DE LA REUNIÓN]. Extrae: decisiones, dueños y deadlines. Crea una tarea en la base Tasks por cada punto accionable, con responsable y fecha. Formato: tareas creadas (título | responsable | fecha).
```

## Tareas programadas (trabajan mientras duermes)
_Tres programas ya configurados en ChatGPT (requiere plan con tareas programadas)._

### 7. Resumen diario de noticias de IA
- Herramienta: ChatGPT programado · cada día 8:00 — [Este modo de ChatGPT trabaja mientras duermes (Tip #30)](https://senalabierta.pages.dev/v/este-modo-de-chatgpt-trabaja-mientras-duermes-tip-30/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Configúralo una vez; llega solo cada mañana.
- Variables: Sin variables. Añade 'en español' o 'foco en [SECTOR]' si lo quieres más concreto.
- Truco: Empieza con UNA tarea programada; añade la segunda cuando la primera te resulte útil.

```
Cada día a las 8:00, resume las 5 noticias de IA más importantes de hoy. Cada una en 3 líneas: qué pasó, por qué importa y la fuente. Si no hay noticias relevantes, dilo en una línea y no rellenes.
```

### 8. Comparador semanal de precios
- Herramienta: ChatGPT programado · cada lunes — [Este modo de ChatGPT trabaja mientras duermes (Tip #30)](https://senalabierta.pages.dev/v/este-modo-de-chatgpt-trabaja-mientras-duermes-tip-30/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Si pagas varias suscripciones de software.
- Variables: [PLANES] = p.ej. ChatGPT Plus, Claude Pro, Gemini Advanced. [DESCRIBE TU USO] = intensidad real.
- Truco: Pega tu factura real de cada plan: la comparación deja de ser genérica.

```
Cada lunes, compara estos planes: [PLANES]. Según mi uso actual ([DESCRIBE TU USO]), dime cuál conviene y en cuánto ahorrarías al mes. Formato: tabla (plan | precio | encaje | recomendación) en máximo 6 líneas.
```

### 9. Coach de hábitos nocturno
- Herramienta: ChatGPT programado · cada noche — [Este modo de ChatGPT trabaja mientras duermes (Tip #30)](https://senalabierta.pages.dev/v/este-modo-de-chatgpt-trabaja-mientras-duermes-tip-30/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Antes de dormir: te pregunta, tú respondes en 30 segundos.
- Variables: [LISTA DE HÁBITOS] = 2-4 hábitos máximo (p.ej. 'entrenar', 'leer 20 min', 'sin redes antes de dormir').
- Truco: La nota de 7 días seguidos es tu foto real de constancia: mira la tendencia, no el día suelto.

```
Cada noche, pregúntame qué completé de mis hábitos de hoy: [LISTA DE HÁBITOS]. Dame una nota del 1 al 10 y un consejo concreto para mañana, en un máximo de 3 líneas. Sin sermón, sin culpa.
```

## Investigación y aprendizaje
_De horas de búsqueda a resultados con fuente y fecha._

### 10. Analista senior en 30 segundos (Perplexity)
- Herramienta: Perplexity — [Prompt único: Perplexity investiga por ti (Tip #57)](https://senalabierta.pages.dev/v/prompt-unico-perplexity-investiga-por-ti-en-30-seg-tip-57/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Cualquier tema que hoy te haría pasar por Google una hora.
- Variables: [TEMA] = p.ej. 'precios de los competidores de Notion'. Añade 'solo fuentes de [AÑO]' para acotar.
- Truco: El punto 4 (contrargumentos) es lo que separa un resumen de un análisis: úsalo siempre.

```
Actúa como analista senior. Investiga [TEMA]. Entrega: 1) Resumen ejecutivo de 200 palabras, 2) 5 hallazgos clave con fuente y fecha, 3) 3 métricas o datos duros, 4) contrargumentos a la conclusión principal, 5) próximos pasos. Formato: tabla markdown.
```

### 11. Tutor Feynman en 7 días
- Herramienta: ChatGPT — [Aprende cualquier skill en 1/10 del tiempo (Tip #13)](https://senalabierta.pages.dev/v/aprende-cualquier-skill-en-1-10-del-tiempo-prompt-feynman-tip-13/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Cuando decidas aprender algo nuevo (SQL, React, copywriting, negociación...).
- Variables: [TEMA] = lo que quieras aprender. [NIVEL] = sé honesto con tu nivel real.
- Truco: Responde a las 5 preguntas socráticas ANTES de seguir: ahí están tus huecos de verdad.

```
Actúa como tutor Feynman. Tema: [TEMA]. Nivel actual: [PRINCIPIANTE/INTERMEDIO]. Entrega: 1) explicación simple, como a un niño de 12 años, 2) 3 analogías cotidianas, 3) 5 preguntas socráticas para detectar mis huecos, 4) 3 ejercicios de práctica progresiva, 5) recursos curados (gratis y de pago). Formato: plan de estudio de 7 días.
```

### 12. Curador de 10 fuentes con fecha
- Herramienta: ChatGPT / Perplexity — [Escribí 50 newsletters en 2h con este sistema (Tip #19)](https://senalabierta.pages.dev/v/escribi-50-newsletters-en-2h-con-este-sistema-tip-19/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Fase 1 de cualquier newsletter, informe o artículo.
- Variables: [TEMA] = el tema de tu próxima newsletter o artículo.
- Truco: Exige fecha: una fuente de hace 3 años en IA ya es historia.

```
Tema: [TEMA]. Busca 10 fuentes de los últimos 12 meses. Entrega una tabla markdown con: título del artículo, 1 insight clave, enlace y fecha. Prioriza fuentes primarias (informes, datos oficiales, autores del sector) y descarta blogs sin autor verificable.
```

## Tu carrera en automático
_De buscar a ser elegido: 10 horas semanales de portales pasan a 30 minutos._

### 13. Perfil maestro de búsqueda de empleo
- Herramienta: ChatGPT — [Esta IA encuentra trabajos que tardarías horas (Tip #52)](https://senalabierta.pages.dev/v/esta-ia-encuentra-trabajos-que-tardarias-horas-en-buscar-tip-52/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Única vez, al empezar tu búsqueda. El resto del flujo parte de aquí.
- Variables: [...] = tu situación real, incluido salario mínimo (evita perder el tiempo en ofertas fuera de rango).
- Truco: Guarda esta conversación: es la base de la que cuelgan los dos prompts siguientes.

```
Este es mi perfil: [AÑOS DE EXPERIENCIA, ROLES, HABILIDADES, SALARIO MÍNIMO, PREFERENCIA REMOTO/HÍBRIDO]. Esto es lo que busco: [TIPO DE PUESTO]. Eres mi agente de empleo: esta información es tu criterio de filtrado permanente. Confírmame en 5 líneas que entendiste el perfil y dime qué descartarías de entrada.
```

### 14. Rastreador matutino de ofertas
- Herramienta: ChatGPT (con búsqueda) o Perplexity — [Esta IA encuentra trabajos que tardarías horas (Tip #52)](https://senalabierta.pages.dev/v/esta-ia-encuentra-trabajos-que-tardarias-horas-en-buscar-tip-52/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Cada mañana, sobre el perfil del prompt anterior.
- Variables: [TIPO DE PUESTO] = p.ej. 'frontend remoto junior'.
- Truco: El corte de encaje 7+ es la clave: una lista corta y buena se revisa; una larga no se toca.

```
Busca ofertas nuevas de [TIPO DE PUESTO] publicadas en las últimas 24 horas. Filtra con mi perfil: [PEGA EL PERFIL]. Devuelve solo la tabla: puesto | empresa | salario (si aparece) | encaje del 1 al 10 | enlace. Máximo 5 ofertas; si no hay ninguna con encaje 7+, dilo en una línea.
```

### 15. CV adaptado + carta + 5 preguntas de entrevista
- Herramienta: ChatGPT — [Esta IA encuentra trabajos que tardarías horas (Tip #52)](https://senalabierta.pages.dev/v/esta-ia-encuentra-trabajos-que-tardarias-horas-en-buscar-tip-52/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Solo para las 3 mejores ofertas de tu tabla.
- Variables: El CV va íntegro: el adaptador reordena, nunca fablica.
- Truco: Regla anti-mentira: si un logro no está en tu CV, no entra. La entrevista lo pillará.

```
Oferta: [PEGA LA OFERTA]. Mi CV: [PEGA TU CV]. Entrega: 1) versión de tu experiencia adaptada a ESTA oferta, sin inventar nada que no esté en el CV, con logros medibles reordenados por relevancia, 2) carta de presentación de 120 palabras, 3) 5 preguntas probables de entrevista con mi respuesta sugerida basada en el CV. Formato: tres bloques separados.
```

## Copy que convierte
_Un prompt, diez variantes: headlines, emails, anuncios y guion de venta._

### 16. Copywriter direct-response completo
- Herramienta: ChatGPT — [Prompt único: Copy que convierte (Tip #44)](https://senalabierta.pages.dev/v/prompt-unico-copy-que-convierte-copia-y-pega-tip-44/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Lanzamiento de producto, campaña o landing nueva.
- Variables: [PRODUCTO] = tu oferta. [AVATAR] = quién compra. [DOLOR] = qué le quita el sueño. [DESEO] = qué quiere de verdad.
- Truco: Si sale demasiado infomercial, añade al final: 'tono conversacional, sin hype'.

```
Actúa como copywriter senior direct-response. Producto: [PRODUCTO]. Avatar: [AVATAR]. Dolor: [DOLOR]. Deseo: [DESEO]. Entrega: 1) 5 headlines gancho (curiosidad + beneficio), 2) 3 emails de secuencia (gancho -> historia -> oferta), 3) 2 anuncios para Facebook/IG (texto principal + headline), 4) 1 guion de vídeo de venta de 60 segundos. Formato: listo para publicar, sin meta-comentarios.
```

### 17. Fórmula de prompts comerciales (rol + gatillos + CTA)
- Herramienta: ChatGPT — Fórmula de prompts comerciales del canal
- Cuándo: Cuando necesites copy de venta rápido para redes o anuncios.
- Variables: [TIPO DE PRODUCTO], [PRODUCTO], [CLIENTE] = lo que vendas, incluso si es un servicio freelance.
- Truco: Pide '3 variaciones del CTA' y quédate con la que diga lo mismo con menos palabras.

```
Actúa como un vendedor experto con 20 años vendiendo [TIPO DE PRODUCTO]. Producto objetivo: [PRODUCTO]. Cliente ideal: [CLIENTE]. Escribe un copy que use gatillos mentales honestos: prueba social, escasez real y un llamado a la acción directo. Entrega: 1) 3 titulares, 2) párrafo de venta de 80 palabras, 3) CTA final. Sin promesas que no se puedan cumplir.
```

## Tu voz, tus newsletters
_La IA escribe como tú (no como la IA): primero le enseñas tu voz._

### 18. Voice profile (extrae tu voz en JSON)
- Herramienta: ChatGPT — [Escribí 50 newsletters en 2h con este sistema (Tip #19)](https://senalabierta.pages.dev/v/escribi-50-newsletters-en-2h-con-este-sistema-tip-19/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Una vez por cada cambio importante de estilo. Guarda el resultado.
- Variables: [PEGA 5 TEXTOS] = cosas que YA escribiste tú (no textos de la IA).
- Truco: Guarda el JSON como voice.json: es el motor de todo el sistema de newsletters.

```
Analiza estos 5 textos míos: [PEGA 5 NEWSLETTERS O TEXTOS]. Extrae: tono, longitud media de frase, vocabulario favorito, estructura de párrafos y nivel de humor. Entrega JSON con las claves: tone, sentence_length, vocabulary, structure, humor. Y después, en 3 frases en lenguaje llano, qué hace único mi estilo.
```

### 19. Newsletter en tu voz con tus fuentes
- Herramienta: ChatGPT — [Escribí 50 newsletters en 2h con este sistema (Tip #19)](https://senalabierta.pages.dev/v/escribi-50-newsletters-en-2h-con-este-sistema-tip-19/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Fase 2 del sistema, con las fuentes ya curadas.
- Variables: [TABLA DE FUENTES] = la salida del prompt de curación de fuentes.
- Truco: Si suena a IA, añade al final: 'reescribe con más personales y menos adverbios'.

```
Voice: [PEGA voice.json O LAS 3 FRASES DE TU ESTILO]. Fuentes: [PEGA LA TABLA DE 10 FUENTES]. Escribe la newsletter: hook de 1 frase -> 3 insights -> 1 consejo accionable -> CTA. 400 palabras, mi voz, sin relleno, sin frases de manual.
```

## Imágenes y miniaturas
_Seis plantillas para Ideogram (texto impecable) o Midjourney (acabado de cine)._

### 20. Miniatura con texto (el rey: Ideogram)
- Herramienta: Ideogram — [La verdad incómoda sobre la IA que dibuja (Tip #29)](https://senalabierta.pages.dev/v/la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Miniaturas de YouTube con título encima: aquí Midjourney deforma las letras.
- Variables: [SUJETO] = lo que aparece. [TEXTO] = máx. 4 palabras (p.ej. 'IA TE REEMPLAZA').
- Truco: Ideogram escribe bien el texto; Midjourney gana en arte. Para miniaturas con palabras, no lo dudes.

```
Miniatura de YouTube 16:9. Sujeto: [SUJETO], primer plano, iluminación dramática. Texto grande y legible en la parte superior: "[TEXTO DE LA MINIATURA]", tipografía sans-serif bold, alto contraste. Fondo con espacio negativo a la derecha. Sin marcos de agua. Estilo: vibrante, colores saturados.
```

### 21. Retrato cinematográfico
- Herramienta: Midjourney — [La verdad incómoda sobre la IA que dibuja (Tip #29)](https://senalabierta.pages.dev/v/la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Avatares, portadas de personas, imágenes de artículo.
- Variables: [PERSONA/DESCRIPCIÓN] = p.ej. 'una mujer ingeniera de 30 años en un laboratorio'.
- Truco: --style raw quita el embellecimiento por defecto: los rasgos se mantienen fieles.

```
Retrato cinematográfico de [PERSONA/DESCRIPCIÓN], piel texturizada, mirada a cámara, luz de contraclave naranja y azul, profundidad de campo corta, objetivo 85mm, render fotorrealista --ar 4:5 --style raw
```

### 22. Paisaje de fondo
- Herramienta: Midjourney / Ideogram — [La verdad incómoda sobre la IA que dibuja (Tip #29)](https://senalabierta.pages.dev/v/la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Fondos para presentaciones, vídeos o posts.
- Variables: [LUGAR IMAGINARIO] = p.ej. 'valle volcánico al amanecer'.
- Truco: Añade 'sin personas y sin texto' cuando quieras fondo limpio para superponer títulos.

```
Paisaje de [LUGAR IMAGINARIO], hora dorada, niebla baja entre las montañas, composición en capas, colores teal y ámbar, estilo matte painting de película, detalle alto, sin personas, sin texto --ar 16:9
```

### 23. Logo con texto legible
- Herramienta: Ideogram — [La verdad incómoda sobre la IA que dibuja (Tip #29)](https://senalabierta.pages.dev/v/la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Bocetos de marca (luego un diseñador lo termina).
- Variables: [NOMBRE] = escríbelo exacto, letra por letra: es donde las IA fallan.
- Truco: Genera 4 variantes y elige la que leas bien a tamaño de favicon.

```
Logotipo minimalista para [TIPO DE NEGOCIO], símbolo [SÍMBOLO O IDEA], tipografía geométrica sans-serif, nombre exacto del negocio: "[NOMBRE]", fondo blanco, colores [2 COLORES], vectores limpios, sin degradados, sin sombras --ar 1:1
```

### 24. Estilo anime
- Herramienta: Midjourney — [La verdad incómoda sobre la IA que dibuja (Tip #29)](https://senalabierta.pages.dev/v/la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Ilustraciones de personajes, posteos creativos, arte de canal.
- Variables: [SHONEN/...] = el subgénero. [ESCENA] = la acción concreta.
- Truco: Para un personaje recurrente del canal, guarda su descripción física y répítela en cada prompt.

```
Ilustración anime estilo [SHONEN/SLICE-OF-LIFE/CIBERPUNK] de [ESCENA], expresión [EMOCIÓN], cabello al viento, fondo bokeh de [LUGAR], líneas limpias, colores vivos, iluminación suave de contraluz, alta calidad --ar 3:4
```

### 25. Fotorealismo de producto
- Herramienta: Midjourney — [La verdad incómoda sobre la IA que dibuja (Tip #29)](https://senalabierta.pages.dev/v/la-verdad-incomoda-sobre-la-ia-que-dibuja-tip-29/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Mockups de producto, imágenes de post o landing sin sesion de fotos.
- Variables: [PRODUCTO] = p.ej. 'auriculares inalámbricos blancos'. [SUPERFICIE] = 'una mesa de mármol'.
- Truco: Midjourney brilla en fotorealismo: aquí no compites con Ideogram, compites con un estudio.

```
Fotografía de producto: [PRODUCTO] sobre [SUPERFICIE], luz de estudio suave desde la izquierda, sombra natural, reflejos controlados, fondo limpio [COLOR], detalle macro, aspecto premium, sin texto, sin logos de terceros --ar 4:3 --style raw
```

## Presentaciones y reuniones
_Del documento de 20 páginas a slides para mañana; de la reunión a tareas sin teclado._

### 26. Doc entero a presentación (Gamma)
- Herramienta: Gamma — [Convierte cualquier doc en presentación (Tip #39)](https://senalabierta.pages.dev/v/convierte-cualquier-doc-en-presentacion-prompt-gamma-tip-39/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Tienes el informe y la reunión es mañana.
- Variables: [N] = 8-12. [AUDIENCIA] = inversores / equipo / clientes. [ESTILO] = según tu marca.
- Truco: Pega el doc completo dentro del prompt (o adjúntalo): la calidad del slide sale de ahí.

```
Transforma este documento en presentación de [N] slides para [AUDIENCIA]. Estructura: 1) hook (problema + promesa), 2-3) contexto clave solo accionable, 4-8) solución o insights (1 idea por slide, con apoyo visual), 9) prueba o caso real, 10) próximos pasos + CTA. Estilo: [MINIMALISTA/CORPORATIVO/CREATIVO]. Elimina relleno. Máximo 40 palabras por slide. Incluye notas del orador por slide.
```

### 27. Project brief automático
- Herramienta: Notion IA — [3 templates Notion IA que uso diario](https://senalabierta.pages.dev/v/3-templates-notion-ia-que-uso-diario-duplica-y-listo/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Al abrir cualquier proyecto nuevo en Notion.
- Variables: [PÁGINA DEL PROYECTO] = enlázala o pega sus notas sueltas.
- Truco: La sección 'qué NO es' es la que evita el scope creep: no la quites nunca.

```
Contexto de este proyecto: [PÁGINA DEL PROYECTO]. Escribe el brief: objetivo, alcance (qué es y qué NO es), stakeholders, riesgos, timeline y definition of done. Formato: las 6 secciones con viñetas, máximo 15 líneas en total.
```

### 28. Reunión a tareas en JSON (Fireflies)
- Herramienta: Fireflies · Custom App — [Prompt Fireflies: de transcripción a tasks en Notion](https://senalabierta.pages.dev/v/prompt-fireflies-de-transcripcion-a-tasks-en-notion-auto/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Una vez configurado, corre solo tras cada reunión.
- Variables: Configúralo en Fireflies > AI Apps > Custom App > auto-run tras la llamada; conecta el webhook a Notion.
- Truco: Añade el campo related_project para auto-enlazar con tu base de proyectos en Notion.

```
Analiza esta reunión. Entrega JSON estricto con: decisions, action_items (con responsable y fecha límite), blockers y followups. Solo incluye lo dicho explícitamente; no infieras. Si no hay nada en una categoría, devuelve la lista vacía.
```

### 29. Resumen ejecutivo de 3 bullets (para Slack)
- Herramienta: ChatGPT / Notion IA — [3 templates Notion IA que uso diario](https://senalabierta.pages.dev/v/3-templates-notion-ia-que-uso-diario-duplica-y-listo/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Cuando necesites avisar al equipo sin escribir el aviso.
- Variables: [PEGA] = informe, transcripción o hilo largo.
- Truco: Si algún bullet supera las 12 palabras, no es un bullet: pídelo más corto.

```
Resume esto en 3 bullets para Slack, para alguien que no ha leído nada de lo anterior: [PEGA EL TEXTO O LA TRANSCRIPCIÓN]. Cada bullet: qué pasó -> qué implica -> qué se espera de quien lo lea. Sin saludo, sin cierre, sin emojis.
```

## Código con contexto (nivel senior)
_La diferencia entre novato y senior no es el modelo: es el contexto que le das._

### 30. Generador con contexto completo (service + tests + migración)
- Herramienta: ChatGPT / Claude / Copilot — [Cómo usan ChatGPT los devs senior (Tip #14)](https://senalabierta.pages.dev/v/como-usan-chatgpt-los-devs-senior-vs-novatos-tip-14/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)
- Cuándo: Feature nueva en un repo existente: el output sale listo para merge.
- Variables: [ESTRUCTURA DEL REPO] = árbol de carpetas + 1-2 ejemplos de módulos ya existentes.
- Truco: Nivel 1: 'hazme una API' da código genérico. Nivel 2: añades el stack y quedan decisiones implícitas. Este es el nivel 3: contexto completo, ahorra 2-4h por feature.

```
Repo: [ESTRUCTURA DEL REPO]. Patterns: repository + service. Convenciones: types estrictos, docstrings estilo Google. Edge cases a cubrir: rate limit, idempotencia. Genera: [FEATURE], con tests y migración si toca. Asume que el código pasa el linter del repo sin tocar su configuración.
```

## Bonus: 3 recetas de vídeo

### Receta con foto de tu nevera (Gemini) — [Gemini cocina con lo de TU nevera (Tip #73)](https://senalabierta.pages.dev/v/gemini-cocina-con-lo-de-tu-nevera-solo-con-una-foto-tip-73/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)

Foto de la nevera -> Gemini la adjunta -> pide: 'Con lo que ves, dame 3 recetas, cuánto tarda cada una y qué ingredientes me faltan'. Funciona también con armarios, facturas en otro idioma o cualquier cosa fotografiada.

### Canción en 2 minutos (Suno) — [Hice una CANCION con IA (Tip #72)](https://senalabierta.pages.dev/v/hice-una-cancion-con-ia-en-2-minutos-escucha-esto-tip-72/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)

Describe estilo + escribe la letra (o pide que la invente) -> genera -> descarga. Plan gratis con créditos diarios. Sirve para regalos, tu negocio o tu primer single.

### Fondos y b-roll gratis (Veo 3 en Shorts) — [Veo 3 genera video CON sonido (Tip #45)](https://senalabierta.pages.dev/v/nuevo-veo-3-genera-video-con-sonido-gratis-en-shorts-tip-45/?utm_source=kofi&utm_medium=shop&utm_campaign=pack30)

En la app de YouTube: Crear -> Efectos -> IA. Describe la escena (p.ej. 'oficina futurista de noche') y genera el clip con sonido en segundos. Perfecto para fondos y hooks de 3 segundos; se etiqueta como contenido IA.
