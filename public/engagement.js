(() => {
  if (location.protocol !== 'https:' || location.hostname !== 'neon-empanada-519607.netlify.app' || window.__makotoLinkTracking) return;
  window.__makotoLinkTracking = true;
  const profiles = new Map([
    ['https://note.com/crisp_auk8183','note_ai'],['https://note.com/rosy_snake7477','note_psychology'],
    ['https://note.com/brave_violet386','note_migaku'],['https://note.com/shinjitsu_saigen','note_savings'],
    ['https://x.com/abp12f','x'],['https://www.tiktok.com/@otokomigaki.lab2','tiktok'],
    ['https://www.instagram.com/shinjitsu_aiai','instagram']
  ]);
  document.addEventListener('click', event => {
    const anchor=event.target?.closest?.('a[href]');
    if (!anchor || typeof window.gtag !== 'function') return;
    let url;try {url=new URL(anchor.href);}catch{return;}
    let placement='',contentId='';
    if (anchor.closest('#recommended-articles')) placement='recommended';
    else if (anchor.closest('#latest-articles')) placement='latest';
    else if (anchor.closest('#links') || anchor.closest('#social')) placement='sns';
    else if (anchor.closest('#approved-offers')) placement='offer';
    else return;
    const profile=profiles.get(url.origin+url.pathname.replace(/\/$/,''));
    if (placement==='sns') {if (!profile)return;contentId=profile;}
    else if (placement==='offer') {contentId=anchor.dataset.offerId;if(!/^[a-z0-9-]{1,70}$/.test(contentId||''))return;}
    else {
      const match=url.hostname==='note.com'&&url.pathname.match(/^\/(crisp_auk8183|rosy_snake7477|brave_violet386|shinjitsu_saigen)\/n\/(n[a-f0-9]+)\/?$/);
      if(!match)return;contentId=match[2];
    }
    // Send identifiers only: no article titles, query strings or personal input.
    window.gtag('event','hub_link_click',{placement,content_id:contentId,transport_type:'beacon'});
    // Never prevent navigation or wait for Analytics.
  });
})();
