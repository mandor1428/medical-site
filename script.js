const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.primary-nav');

if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!open));
    navigation.classList.toggle('is-open', !open);
  });

  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a') && window.matchMedia('(max-width: 760px)').matches) {
      menuButton.setAttribute('aria-expanded', 'false');
      navigation.classList.remove('is-open');
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      menuButton.setAttribute('aria-expanded', 'false');
      navigation.classList.remove('is-open');
      menuButton.focus();
    }
  });
}

const quoteCounts = [...document.querySelectorAll('[data-quote-count]')];
const toast = document.querySelector('.toast');
let quoteCount = Number(quoteCounts[0]?.textContent || 12);
let toastTimer;

function announce(message) {
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('is-visible');
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove('is-visible'), 2200);
}

document.querySelectorAll('.add-quote').forEach((button) => {
  const productName = button.closest('.product-card')?.querySelector('h3')?.textContent.trim() || 'Prodotto';
  button.setAttribute('aria-label', `Aggiungi ${productName} alla lista quotazione`);

  button.addEventListener('click', () => {
    const added = button.classList.toggle('is-added');
    quoteCount += added ? 1 : -1;
    quoteCounts.forEach((count) => { count.textContent = String(quoteCount); });
    button.innerHTML = added
      ? '<svg aria-hidden="true"><use href="#i-check"></use></svg>Aggiunto alla lista'
      : '<svg aria-hidden="true"><use href="#i-list"></use></svg>Aggiungi alla lista';
    button.setAttribute('aria-pressed', String(added));
    announce(added ? `${productName} aggiunto alla lista` : `${productName} rimosso dalla lista`);
  });
});

const searchForm = document.querySelector('.hero-search');
const searchInput = document.querySelector('#home-search');
if (searchForm && searchInput) {
  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const term = searchInput.value.trim().toLocaleLowerCase('it');
    if (!term) {
      searchInput.focus();
      announce('Inserisci un termine di ricerca');
      return;
    }

    const category = [...document.querySelectorAll('.category-card')]
      .find((card) => card.textContent.toLocaleLowerCase('it').includes(term));
    document.querySelector('#categorie')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (category) {
      category.focus({ preventScroll: true });
      category.classList.add('search-match');
      window.setTimeout(() => category.classList.remove('search-match'), 1800);
      announce(`Categoria trovata: ${category.querySelector('strong')?.textContent || term}`);
    } else {
      announce(`Ricerca pronta per “${searchInput.value.trim()}”`);
    }
  });
}
