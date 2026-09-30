(() => {
  'use strict';

  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  const YT_RE = /^[A-Za-z0-9_-]{6,20}$/;

  const mount = (box) => {
    const id = box.getAttribute('data-yt');
    if (!YT_RE.test(id)) return;
    const frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
    frame.title = box.getAttribute('aria-label') || 'Reproductor de YouTube';
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.allowFullscreen = true;
    box.replaceChildren(frame);
    box.classList.add('is-playing');
    box.removeAttribute('role');
    box.removeAttribute('tabindex');
  };

  document.querySelectorAll('[data-yt]').forEach((box) => {
    box.addEventListener('click', () => mount(box), { once: true });
    box.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        mount(box);
      }
    });
  });
})();
