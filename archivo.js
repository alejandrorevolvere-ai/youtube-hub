(() => {
  'use strict';

  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  const grid = document.getElementById('arch-grid');
  if (!grid) return;
  const cards = Array.from(grid.querySelectorAll('.vcard'));
  const empty = document.querySelector('.arch-empty');
  const countEl = document.querySelector('[data-arch-count]');
  const input = document.getElementById('arch-q');
  const buttons = Array.from(document.querySelectorAll('[data-filter]'));

  const state = { channel: 'all', query: '' };

  const apply = () => {
    const q = state.query.trim().toLowerCase();
    let shown = 0;
    cards.forEach((card) => {
      const chOk = state.channel === 'all' || card.dataset.ch === state.channel;
      const title = (card.querySelector('.vtitle') || {}).textContent || '';
      const qOk = !q || title.toLowerCase().indexOf(q) !== -1;
      const visible = chOk && qOk;
      card.hidden = !visible;
      if (visible) shown += 1;
    });
    if (countEl) countEl.textContent = String(shown);
    if (empty) empty.hidden = shown !== 0;
  };

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      state.channel = btn.dataset.filter || 'all';
      buttons.forEach((b) => b.classList.toggle('is-on', b === btn));
      apply();
    });
  });

  if (input) {
    let timer = 0;
    input.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => { state.query = input.value; apply(); }, 120);
    });
    input.addEventListener('keydown', (e) => { if (e.key === 'Escape') { input.value = ''; state.query = ''; apply(); } });
  }

  apply();
})();
