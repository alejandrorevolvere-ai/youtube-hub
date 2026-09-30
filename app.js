(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const revealEls = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealEls.forEach((el) => el.classList.add('is-in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach((el) => io.observe(el));
  }

  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  const fmt = (n) => n.toLocaleString('es-ES');
  const countUp = (el) => {
    const target = Number(el.getAttribute('data-count'));
    if (!Number.isFinite(target)) return;
    if (reduceMotion) { el.textContent = fmt(target); return; }
    const duration = 900;
    const start = performance.now();
    const step = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const counters = document.querySelectorAll('[data-count]');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    counters.forEach(countUp);
  } else {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          countUp(entry.target);
          cio.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach((el) => cio.observe(el));
  }

  const VID_RE = /^[A-Za-z0-9_-]{6,20}$/;
  const isInt = (v) => Number.isInteger(v) && v >= 0;
  const UTM = 'utm_source=youtube_hub&utm_medium=link&utm_campaign=senal_abierta';

  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };

  const monthShort = (iso) => {
    const d = new Date(iso + 'T00:00:00Z');
    if (Number.isNaN(d.getTime())) return '';
    const meses = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'];
    return d.getUTCDate() + ' ' + meses[d.getUTCMonth()];
  };

  const buildCard = (v, chKey, chName, tagClass) => {
    if (!v || typeof v.id !== 'string' || !VID_RE.test(v.id)) return null;
    const href = 'https://www.youtube.com/watch?v=' + v.id + '&' + UTM + '&utm_content=vcard';
    const title = typeof v.title === 'string' ? v.title.slice(0, 120) : '';

    const card = el('a', 'vcard reveal is-in');
    card.href = href;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.dataset.vid = v.id;
    card.dataset.ch = chKey;
    if (typeof v.published === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v.published)) {
      card.dataset.pub = v.published;
    }

    const thumb = el('span', 'vthumb');
    const img = el('img');
    img.src = 'https://i.ytimg.com/vi/' + v.id + '/hqdefault.jpg';
    img.alt = title;
    img.loading = 'lazy';
    thumb.appendChild(img);
    thumb.appendChild(el('span', 'vtag ' + tagClass, chName));
    thumb.appendChild(el('span', 'vplay', '▶'));
    card.appendChild(thumb);

    const body = el('span', 'vcard-body');
    body.appendChild(el('span', 'vtitle', title));
    const meta = el('span', 'vmeta');
    if (typeof v.published === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v.published)) {
      meta.appendChild(el('span', 'data-date', monthShort(v.published)));
    }
    meta.appendChild(el('span', null, 'Ver en YouTube ↗'));
    body.appendChild(meta);
    card.appendChild(body);
    return card;
  };

  const applyData = (data) => {
    if (!data || typeof data !== 'object' || typeof data.channels !== 'object' || !data.channels) return;

    const stamp = document.querySelector('[data-stamp]');
    if (stamp && typeof data.generated_at === 'string' && /^\d{4}-\d{2}-\d{2}/.test(data.generated_at)) {
      stamp.textContent = data.generated_at.slice(0, 10).replace(/-/g, '.');
    }

    const map = { club: { card: 0, tag: 'vtag-club' }, ia60: { card: 1, tag: 'vtag-ia' } };
    const channelCards = document.querySelectorAll('.channel-card');
    let totals = { videos: 0, views: 0, subs: 0, ok: false };

    Object.keys(map).forEach((key) => {
      const ch = data.channels[key];
      if (!ch || typeof ch !== 'object') return;
      const info = map[key];
      const card = channelCards[info.card];
      if (card) {
        const stats = card.querySelectorAll('.channel-stats strong');
        if (isInt(ch.subscribers) && stats[0]) {
          stats[0].setAttribute('data-count', String(ch.subscribers));
          stats[0].textContent = fmt(ch.subscribers);
        }
        if (isInt(ch.videos) && stats[1]) {
          stats[1].setAttribute('data-count', String(ch.videos));
          stats[1].textContent = fmt(ch.videos);
        }
        if (isInt(ch.views) && stats[2]) {
          stats[2].setAttribute('data-count', String(ch.views));
          stats[2].textContent = fmt(ch.views);
        }
      }
      if (isInt(ch.videos) && isInt(ch.views) && isInt(ch.subscribers)) {
        totals.videos += ch.videos;
        totals.views += ch.views;
        totals.subs += ch.subscribers;
        totals.ok = true;
      }
    });

    const heroStats = document.querySelectorAll('.hero-stats strong');
    if (totals.ok && heroStats.length === 3) {
      const vals = [totals.videos, totals.views, totals.subs];
      vals.forEach((v, i) => {
        heroStats[i].setAttribute('data-count', String(v));
        heroStats[i].textContent = fmt(v);
      });
    }

    const grid = document.getElementById('vgrid');
    if (!grid || grid.children.length === 0) return;
    const picks = [];
    ['club', 'ia60'].forEach((key) => {
      const ch = data.channels[key];
      if (ch && Array.isArray(ch.latest)) {
        ch.latest.slice(0, 4).forEach((v) => picks.push({ v: v, key: key }));
      }
    });
    if (picks.length === 0) return;
    picks.sort((a, b) => {
      const da = typeof a.v.published === 'string' ? a.v.published : '';
      const db = typeof b.v.published === 'string' ? b.v.published : '';
      return db.localeCompare(da);
    });
    const chMeta = { club: ['El Club del Negocio', 'vtag-club'], ia60: ['IA en 60"', 'vtag-ia'] };
    const frag = document.createDocumentFragment();
    picks.slice(0, 8).forEach((p) => {
      const meta = chMeta[p.key];
      const node = buildCard(p.v, p.key, meta[0], meta[1]);
      if (node) frag.appendChild(node);
    });
    if (frag.childNodes.length > 0) {
      grid.replaceChildren(frag);
    }
  };

  if (window.fetch && typeof document.getElementById === 'function') {
    fetch('data.json', { credentials: 'same-origin' })
      .then((r) => { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
      .then(applyData)
      .catch(() => { /* sin data.json se mantiene el HTML estático */ });
  }
})();
