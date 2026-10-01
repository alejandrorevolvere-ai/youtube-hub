# -*- coding: utf-8 -*-
"""Contenido del pack: secciones 1-4 (productividad, programadas, investigación, carrera)."""
from links import link

SECTIONS_A = [
    {
        "title": "Productividad y organización",
        "intro": "Menos gestión, más resultado. Estos 6 prompts cubren la semana completa de trabajo.",
        "prompts": [
            {
                "title": "Planificador semanal (chief of staff)",
                "tool": "ChatGPT",
                "source": "3 prompts que me ahorran 10h/semana (Tip #50)",
                "url": link("3-prompts-de-chatgpt-que-me-ahorran-10h-semana-tip-50"),
                "when": "Los domingos por la noche o los lunes a primera hora.",
                "text": "Actúa como mi chief of staff. Aquí están mis metas del mes: [METAS]. "
                        "Mi disponibilidad es [HORAS LIBRES]. Genera un plan día por día de esta semana "
                        "con bloques de 90 minutos, priorizando lo que más acerca mis metas. "
                        "Marca 1 bloque de foco profundo al día y 1 margen para imprevistos. "
                        "Formato: tabla (día | bloque | tarea | resultado esperado).",
                "vars": "[METAS] = tus 2-3 objetivos. [HORAS LIBRES] = huecos reales de tu semana.",
                "truco": "Pega la lista de tareas que ya tengas: el plan sale realista en el primer intento.",
            },
            {
                "title": "Procesador de emails (suena a ti)",
                "tool": "ChatGPT",
                "source": "3 prompts que me ahorran 10h/semana (Tip #50)",
                "url": link("3-prompts-de-chatgpt-que-me-ahorran-10h-semana-tip-50"),
                "when": "Cuando tengas 10+ emails pendientes: pega los 10 de golpe.",
                "text": "Responde cada email como yo. Mi relación con el remitente: [CONTEXTO]. "
                        "Tono: directo, empático, con acción clara. Máximo 3 líneas por respuesta. "
                        "Sin relleno, sin disculpas inventadas, sin prometer lo que no puedo cumplir.\n\n"
                        "Emails:\n[PEGA EMAILS]",
                "vars": "[CONTEXTO] = 'cliente', 'jefe', 'proveedor'... [PEGA EMAILS] = numerados (1., 2., 3.).",
                "truco": "Revisa y ajusta antes de enviar: el 90% sirve tal cual, el 10% final lo personalizas tú.",
            },
            {
                "title": "Resumen de reuniones (decisiones + tareas)",
                "tool": "ChatGPT / Notion IA",
                "source": "3 prompts que me ahorran 10h/semana (Tip #50)",
                "url": link("3-prompts-de-chatgpt-que-me-ahorran-10h-semana-tip-50"),
                "when": "En cuanto termine cualquier reunión con transcripción.",
                "text": "Transcripción: [PEGA TRANSCRIPCIÓN]. Extrae: 1) 3 decisiones tomadas, "
                        "2) 5 action items con responsable y fecha, 3) riesgos o bloqueos abiertos. "
                        "Solo lo que aparece explícito en la transcripción; no infieras ni rellenes huecos. "
                        "Formato: tres tablas separadas.",
                "vars": "[PEGA TRANSCRIPCIÓN] = la de Zoom/Meet/Teams/Fireflies.",
                "truco": "Añade 'y una frase: ¿quedó claro el siguiente paso?' para detectar reuniones mal cerradas.",
            },
            {
                "title": "Inbox a cero (segundo cerebro)",
                "tool": "Notion IA",
                "source": "Mi segundo cerebro en Notion IA (Tip #66)",
                "url": link("mi-segundo-cerebro-en-notion-ia-captura-organiza-acciona-tip-66"),
                "when": "Cada noche, con tu base Inbox de Notion.",
                "text": "Revisa la base Inbox. Mueve cada item a su proyecto o área. "
                        "Crea tareas con fecha para todo lo accionable. "
                        "Resume en una línea los items que requieran más de 5 minutos de lectura. "
                        "Responde solo con la lista de cambios realizados.",
                "vars": "Sin variables: funciona directo sobre tu base Inbox.",
                "truco": "Si tu Inbox supera los 30 items, ejecútalo dos noches seguidas hasta dejarlo limpio.",
            },
            {
                "title": "Plan del día con tus reuniones",
                "tool": "Notion IA",
                "source": "3 templates Notion IA que uso diario",
                "url": link("3-templates-notion-ia-que-uso-diario-duplica-y-listo"),
                "when": "Botón 'Plan IA' en tu Daily Planner, cada mañana.",
                "text": "Lee mis reuniones de hoy y mis tareas abiertas. "
                        "Genera: 3 prioridades del día, bloques de tiempo y margen de buffer entre reuniones. "
                        "Formato: horario del día, de la primera reunión a la última.",
                "vars": "Sin variables: conecta el botón a tu calendario y base de tareas.",
                "truco": "Regla de las 3 prioridades: si el día solo dejara tiempo para 3 cosas, ¿cuáles serían?",
            },
            {
                "title": "Action items desde transcripción (a tu base Tasks)",
                "tool": "Notion IA",
                "source": "3 templates Notion IA que uso diario",
                "url": link("3-templates-notion-ia-que-uso-diario-duplica-y-listo"),
                "when": "Botón 'Action items' sobre cualquier reunión transcrita.",
                "text": "Transcripción: [PROPIEDAD DE LA REUNIÓN]. Extrae: decisiones, dueños y deadlines. "
                        "Crea una tarea en la base Tasks por cada punto accionable, con responsable y fecha. "
                        "Formato: tareas creadas (título | responsable | fecha).",
                "vars": "[PROPIEDAD DE LA REUNIÓN] = el texto de la transcripción pegado en la página.",
                "truco": "Añade 'relaciona cada tarea con su proyecto' para mantener tu tabla Projects viva.",
            },
        ],
    },
    {
        "title": "Tareas programadas (trabajan mientras duermes)",
        "intro": "Tres programas ya configurados en ChatGPT (requiere plan con tareas programadas).",
        "prompts": [
            {
                "title": "Resumen diario de noticias de IA",
                "tool": "ChatGPT programado · cada día 8:00",
                "source": "Este modo de ChatGPT trabaja mientras duermes (Tip #30)",
                "url": link("este-modo-de-chatgpt-trabaja-mientras-duermes-tip-30"),
                "when": "Configúralo una vez; llega solo cada mañana.",
                "text": "Cada día a las 8:00, resume las 5 noticias de IA más importantes de hoy. "
                        "Cada una en 3 líneas: qué pasó, por qué importa y la fuente. "
                        "Si no hay noticias relevantes, dilo en una línea y no rellenes.",
                "vars": "Sin variables. Añade 'en español' o 'foco en [SECTOR]' si lo quieres más concreto.",
                "truco": "Empieza con UNA tarea programada; añade la segunda cuando la primera te resulte útil.",
            },
            {
                "title": "Comparador semanal de precios",
                "tool": "ChatGPT programado · cada lunes",
                "source": "Este modo de ChatGPT trabaja mientras duermes (Tip #30)",
                "url": link("este-modo-de-chatgpt-trabaja-mientras-duermes-tip-30"),
                "when": "Si pagas varias suscripciones de software.",
                "text": "Cada lunes, compara estos planes: [PLANES]. "
                        "Según mi uso actual ([DESCRIBE TU USO]), dime cuál conviene y en cuánto ahorrarías "
                        "al mes. Formato: tabla (plan | precio | encaje | recomendación) en máximo 6 líneas.",
                "vars": "[PLANES] = p.ej. ChatGPT Plus, Claude Pro, Gemini Advanced. [DESCRIBE TU USO] = intensidad real.",
                "truco": "Pega tu factura real de cada plan: la comparación deja de ser genérica.",
            },
            {
                "title": "Coach de hábitos nocturno",
                "tool": "ChatGPT programado · cada noche",
                "source": "Este modo de ChatGPT trabaja mientras duermes (Tip #30)",
                "url": link("este-modo-de-chatgpt-trabaja-mientras-duermes-tip-30"),
                "when": "Antes de dormir: te pregunta, tú respondes en 30 segundos.",
                "text": "Cada noche, pregúntame qué completé de mis hábitos de hoy: [LISTA DE HÁBITOS]. "
                        "Dame una nota del 1 al 10 y un consejo concreto para mañana, "
                        "en un máximo de 3 líneas. Sin sermón, sin culpa.",
                "vars": "[LISTA DE HÁBITOS] = 2-4 hábitos máximo (p.ej. 'entrenar', 'leer 20 min', 'sin redes antes de dormir').",
                "truco": "La nota de 7 días seguidos es tu foto real de constancia: mira la tendencia, no el día suelto.",
            },
        ],
    },
    {
        "title": "Investigación y aprendizaje",
        "intro": "De horas de búsqueda a resultados con fuente y fecha.",
        "prompts": [
            {
                "title": "Analista senior en 30 segundos (Perplexity)",
                "tool": "Perplexity",
                "source": "Prompt único: Perplexity investiga por ti (Tip #57)",
                "url": link("prompt-unico-perplexity-investiga-por-ti-en-30-seg-tip-57"),
                "when": "Cualquier tema que hoy te haría pasar por Google una hora.",
                "text": "Actúa como analista senior. Investiga [TEMA]. Entrega: "
                        "1) Resumen ejecutivo de 200 palabras, 2) 5 hallazgos clave con fuente y fecha, "
                        "3) 3 métricas o datos duros, 4) contrargumentos a la conclusión principal, "
                        "5) próximos pasos. Formato: tabla markdown.",
                "vars": "[TEMA] = p.ej. 'precios de los competidores de Notion'. Añade 'solo fuentes de [AÑO]' para acotar.",
                "truco": "El punto 4 (contrargumentos) es lo que separa un resumen de un análisis: úsalo siempre.",
            },
            {
                "title": "Tutor Feynman en 7 días",
                "tool": "ChatGPT",
                "source": "Aprende cualquier skill en 1/10 del tiempo (Tip #13)",
                "url": link("aprende-cualquier-skill-en-1-10-del-tiempo-prompt-feynman-tip-13"),
                "when": "Cuando decidas aprender algo nuevo (SQL, React, copywriting, negociación...).",
                "text": "Actúa como tutor Feynman. Tema: [TEMA]. Nivel actual: [PRINCIPIANTE/INTERMEDIO]. "
                        "Entrega: 1) explicación simple, como a un niño de 12 años, "
                        "2) 3 analogías cotidianas, 3) 5 preguntas socráticas para detectar mis huecos, "
                        "4) 3 ejercicios de práctica progresiva, 5) recursos curados (gratis y de pago). "
                        "Formato: plan de estudio de 7 días.",
                "vars": "[TEMA] = lo que quieras aprender. [NIVEL] = sé honesto con tu nivel real.",
                "truco": "Responde a las 5 preguntas socráticas ANTES de seguir: ahí están tus huecos de verdad.",
            },
            {
                "title": "Curador de 10 fuentes con fecha",
                "tool": "ChatGPT / Perplexity",
                "source": "Escribí 50 newsletters en 2h con este sistema (Tip #19)",
                "url": link("escribi-50-newsletters-en-2h-con-este-sistema-tip-19"),
                "when": "Fase 1 de cualquier newsletter, informe o artículo.",
                "text": "Tema: [TEMA]. Busca 10 fuentes de los últimos 12 meses. "
                        "Entrega una tabla markdown con: título del artículo, 1 insight clave, enlace y fecha. "
                        "Prioriza fuentes primarias (informes, datos oficiales, autores del sector) "
                        "y descarta blogs sin autor verificable.",
                "vars": "[TEMA] = el tema de tu próxima newsletter o artículo.",
                "truco": "Exige fecha: una fuente de hace 3 años en IA ya es historia.",
            },
        ],
    },
    {
        "title": "Tu carrera en automático",
        "intro": "De buscar a ser elegido: 10 horas semanales de portales pasan a 30 minutos.",
        "prompts": [
            {
                "title": "Perfil maestro de búsqueda de empleo",
                "tool": "ChatGPT",
                "source": "Esta IA encuentra trabajos que tardarías horas (Tip #52)",
                "url": link("esta-ia-encuentra-trabajos-que-tardarias-horas-en-buscar-tip-52"),
                "when": "Única vez, al empezar tu búsqueda. El resto del flujo parte de aquí.",
                "text": "Este es mi perfil: [AÑOS DE EXPERIENCIA, ROLES, HABILIDADES, "
                        "SALARIO MÍNIMO, PREFERENCIA REMOTO/HÍBRIDO]. Esto es lo que busco: [TIPO DE PUESTO]. "
                        "Eres mi agente de empleo: esta información es tu criterio de filtrado permanente. "
                        "Confírmame en 5 líneas que entendiste el perfil y dime qué descartarías de entrada.",
                "vars": "[...] = tu situación real, incluido salario mínimo (evita perder el tiempo en ofertas fuera de rango).",
                "truco": "Guarda esta conversación: es la base de la que cuelgan los dos prompts siguientes.",
            },
            {
                "title": "Rastreador matutino de ofertas",
                "tool": "ChatGPT (con búsqueda) o Perplexity",
                "source": "Esta IA encuentra trabajos que tardarías horas (Tip #52)",
                "url": link("esta-ia-encuentra-trabajos-que-tardarias-horas-en-buscar-tip-52"),
                "when": "Cada mañana, sobre el perfil del prompt anterior.",
                "text": "Busca ofertas nuevas de [TIPO DE PUESTO] publicadas en las últimas 24 horas. "
                        "Filtra con mi perfil: [PEGA EL PERFIL]. Devuelve solo la tabla: "
                        "puesto | empresa | salario (si aparece) | encaje del 1 al 10 | enlace. "
                        "Máximo 5 ofertas; si no hay ninguna con encaje 7+, dilo en una línea.",
                "vars": "[TIPO DE PUESTO] = p.ej. 'frontend remoto junior'.",
                "truco": "El corte de encaje 7+ es la clave: una lista corta y buena se revisa; una larga no se toca.",
            },
            {
                "title": "CV adaptado + carta + 5 preguntas de entrevista",
                "tool": "ChatGPT",
                "source": "Esta IA encuentra trabajos que tardarías horas (Tip #52)",
                "url": link("esta-ia-encuentra-trabajos-que-tardarias-horas-en-buscar-tip-52"),
                "when": "Solo para las 3 mejores ofertas de tu tabla.",
                "text": "Oferta: [PEGA LA OFERTA]. Mi CV: [PEGA TU CV]. Entrega: "
                        "1) versión de tu experiencia adaptada a ESTA oferta, sin inventar nada que no esté en el CV, "
                        "con logros medibles reordenados por relevancia, "
                        "2) carta de presentación de 120 palabras, "
                        "3) 5 preguntas probables de entrevista con mi respuesta sugerida basada en el CV. "
                        "Formato: tres bloques separados.",
                "vars": "El CV va íntegro: el adaptador reordena, nunca fablica.",
                "truco": "Regla anti-mentira: si un logro no está en tu CV, no entra. La entrevista lo pillará.",
            },
        ],
    },
]
