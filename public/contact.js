(() => {
  'use strict';
  const bar = document.querySelector('.mobile-contact-bar');
  const contact = document.getElementById('contact');
  if (!bar || !contact || !('IntersectionObserver' in window)) return;
  // The primary contact section already exposes both methods when visible.
  new IntersectionObserver(entries => {
    bar.hidden = entries.some(entry => entry.isIntersecting);
  }, {threshold: 0}).observe(contact);
})();
