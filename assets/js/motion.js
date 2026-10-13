(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pressSelector = [
    'button:not([data-filter-backdrop])',
    '.btn',
    '.primary-button',
    '.secondary-button',
    '.compact-button',
    '.add-quote',
    '.quote-link',
    '.download-link',
    '.section-link',
    '.language',
    '.route-row',
    '.pagination a',
    '.gallery-thumb',
    '[role="tab"]'
  ].join(',');

  document.querySelectorAll(pressSelector).forEach((element) => {
    element.classList.add('motion-press');
    if (window.getComputedStyle(element).position === 'static') {
      element.classList.add('motion-ripple-host');
    }
  });

  if (!reducedMotion) {
    document.addEventListener('pointerdown', (event) => {
      if (event.button !== 0) return;
      const target = event.target.closest(pressSelector);
      if (!target || target.matches(':disabled, [aria-disabled="true"]')) return;

      target.classList.add('is-pressing');
      const rect = target.getBoundingClientRect();
      const ripple = document.createElement('span');
      const diameter = Math.max(rect.width, rect.height) * 2;
      ripple.className = 'motion-ripple';
      ripple.setAttribute('aria-hidden', 'true');
      ripple.style.left = `${event.clientX - rect.left}px`;
      ripple.style.top = `${event.clientY - rect.top}px`;
      ripple.style.setProperty('--ripple-scale', String(Math.max(10, diameter / 12)));
      target.append(ripple);
      ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
    }, { passive: true });

    const releasePress = () => {
      document.querySelectorAll('.is-pressing').forEach((element) => element.classList.remove('is-pressing'));
    };
    document.addEventListener('pointerup', releasePress, { passive: true });
    document.addEventListener('pointercancel', releasePress, { passive: true });

    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.target.closest?.(pressSelector)?.classList.add('is-pressing');
    });
    document.addEventListener('keyup', (event) => {
      if (event.key !== 'Enter' && event.key !== ' ') return;
      event.target.closest?.(pressSelector)?.classList.remove('is-pressing');
    });
  }

  const cardSelector = [
    '.category-card',
    '.product-card',
    '.catalog-card',
    '.solution-card',
    '.entity-card',
    '.procedure-card',
    '.case-card',
    '.useful-card',
    '.example-card',
    '.supply-card',
    '.logo-tile'
  ].join(',');

  document.querySelectorAll(cardSelector).forEach((card) => card.classList.add('motion-card'));

  const heroImages = document.querySelectorAll('.hero-photo img, .page-hero__photo img, .category-hero__photo img');
  const heroCopy = document.querySelectorAll([
    '.hero-panel h1',
    '.hero-panel .hero-intro',
    '.hero-panel .hero-search',
    '.hero-panel .hero-assurances',
    '.page-hero__inner h1',
    '.page-hero__inner .page-hero__lead',
    '.page-hero__inner .btn',
    '.page-hero__inner .hero-proof',
    '.page-hero__inner .solutions-proof',
    '.category-hero__copy h1',
    '.category-hero__copy .category-count',
    '.category-hero__copy .category-lead'
  ].join(','));

  if (!reducedMotion) {
    heroImages.forEach((image) => image.classList.add('motion-hero-image'));
    heroCopy.forEach((element, index) => {
      element.classList.add('motion-hero-copy');
      element.style.setProperty('--motion-order', String(index % 5));
    });
  }

  const revealSelector = [
    '.section-title-row',
    '.category-card',
    '.product-card',
    '.catalog-card',
    '.solution-card',
    '.entity-card',
    '.procedure-card',
    '.mepa-step',
    '.case-card',
    '.useful-card',
    '.service-point',
    '.support-item',
    '.example-card',
    '.supply-card',
    '.logo-tile',
    '.accordion-item',
    '.product-panel',
    '.side-panel',
    '.quote-row',
    '.metric',
    '.proof-item'
  ].join(',');

  const revealElements = [...new Set(document.querySelectorAll(revealSelector))]
    .filter((element) => !element.hidden && !element.closest('[hidden]'));

  if (!reducedMotion && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('motion-enhanced');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, { threshold: .08, rootMargin: '0px 0px -7% 0px' });

    revealElements.forEach((element, index) => {
      element.classList.add('motion-reveal');
      element.style.setProperty('--motion-order', String(index % 6));
      const rect = element.getBoundingClientRect();
      if (rect.top < window.innerHeight * .94 && rect.bottom > 0) element.classList.add('is-visible');
      else observer.observe(element);
    });
  } else {
    revealElements.forEach((element) => element.classList.add('is-visible'));
  }

  document.querySelectorAll('[data-quote-count]').forEach((count) => {
    new MutationObserver(() => {
      if (reducedMotion) return;
      count.classList.remove('motion-pop');
      requestAnimationFrame(() => count.classList.add('motion-pop'));
      window.setTimeout(() => count.classList.remove('motion-pop'), 380);
    }).observe(count, { childList: true, characterData: true, subtree: true });
  });
})();
