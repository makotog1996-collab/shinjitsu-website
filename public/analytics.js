(() => {
  // Measure only the live site, keeping previews and local checks out of GA4.
  if (location.protocol !== 'https:' || location.hostname !== 'neon-empanada-519607.netlify.app') return;
  if (window.__makotoGA4Started) return;
  window.__makotoGA4Started = true;

  const measurementId = 'G-76H2G7LD3T';
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  // config sends the default page_view; do not send a second page_view event.
  window.gtag('config', measurementId, {
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });
  const tag = document.createElement('script');
  tag.async = true;
  tag.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(tag);
})();
