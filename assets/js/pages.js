(() => {
  const menu = document.querySelector('[data-menu-toggle]');
  const nav = document.querySelector('[data-primary-nav]');
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });

    nav.addEventListener('click', (event) => {
      if (event.target.closest('a') && window.matchMedia('(max-width: 760px)').matches) {
        menu.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
      }
    });
  }

  document.querySelectorAll('[data-accordion-trigger]').forEach((trigger) => {
    trigger.addEventListener('click', () => {
      const item = trigger.closest('.accordion-item');
      const open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      trigger.setAttribute('aria-expanded', String(open));
      const marker = trigger.querySelector('i');
      if (marker) marker.textContent = open ? '−' : '+';
    });
  });

  const filter = document.querySelector('[data-filter-sheet]');
  const filterOpen = document.querySelector('[data-filter-open]');
  const filterClose = document.querySelector('[data-filter-apply]');
  const backdrop = document.querySelector('[data-filter-backdrop]');
  const setFilter = (open) => {
    if (!filter || !backdrop) return;
    filter.classList.toggle('is-open', open);
    backdrop.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) filter.querySelector('input, button, select')?.focus();
  };
  filterOpen?.addEventListener('click', () => setFilter(true));
  filterClose?.addEventListener('click', () => setFilter(false));
  backdrop?.addEventListener('click', () => setFilter(false));
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    setFilter(false);
    if (menu && nav && nav.classList.contains('is-open')) {
      menu.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      menu.focus();
    }
  });

  document.querySelectorAll('form[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      form.querySelector('.form-status')?.classList.add('is-visible');
    });
  });

  document.querySelectorAll('[data-qty]').forEach((group) => {
    const output = group.querySelector('output');
    group.querySelector('[data-minus]')?.addEventListener('click', () => {
      output.value = String(Math.max(1, Number(output.value) - 1));
    });
    group.querySelector('[data-plus]')?.addEventListener('click', () => {
      output.value = String(Number(output.value) + 1);
    });
  });
})();
