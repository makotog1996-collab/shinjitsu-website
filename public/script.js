(() => {
  'use strict';
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
  const status = document.getElementById('feed-status');
  const cacheKey = 'shinjitsu-notes-v1';
  const dateFormat = new Intl.DateTimeFormat('ja-JP', {timeZone:'Asia/Tokyo',year:'numeric',month:'2-digit',day:'2-digit'});
  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  async function json(url) {
    const response = await fetch(url, {signal:AbortSignal.timeout(10000),credentials:'omit',cache:'no-cache'});
    if (!response.ok) throw new Error('Unavailable');
    const length = Number(response.headers.get('content-length'));
    if (length > 1500000) throw new Error('Oversized data');
    const raw = await response.text();
    if (raw.length > 1500000) throw new Error('Oversized data');
    return JSON.parse(raw);
  }
  function validDate(value) { return typeof value === 'string' && Number.isFinite(Date.parse(value)); }
  function validName(value) { return typeof value === 'string' && value.trim() && value.length <= 300; }
  function safeNotes(data, config) {
    if (data?.schemaVersion !== 1 || !Array.isArray(data.notes)) throw new Error('Invalid data');
    const items = new Map();
    for (const theme of config.notes) {
      const item = data.notes.find(n => n.url === theme.url);
      if (!item || !validName(item.displayName)) continue;
      const articles = (Array.isArray(item.articles) ? item.articles : []).filter(article => {
        try {
          const url = new URL(article.url);
          return url.origin === 'https://note.com' && !url.username && !url.password && !url.search && !url.hash &&
            url.pathname.startsWith(new URL(theme.url).pathname + '/n/') && /^\/[^/]+\/n\/n[a-f0-9]+$/.test(url.pathname) &&
            typeof article.title === 'string' && article.title.trim() && article.title.length <= 1000 && validDate(article.publishedAt);
        } catch { return false; }
      }).slice(0,30);
      items.set(theme.url,{...item,articles});
    }
    if (!items.size) throw new Error('No valid profiles');
    return items;
  }
  let current = new Map();
  function render(data, config, source) {
    const incoming = safeNotes(data, config);
    for (const [url, item] of incoming) {
      const old = current.get(url);
      const oldTime = Date.parse(old?.fetchedAt) || 0;
      const newTime = Date.parse(item.fetchedAt) || 0;
      if (!old || newTime >= oldTime) current.set(url, item);
    }
    for (const node of document.querySelectorAll('[data-note-name]')) {
      const item = current.get(node.dataset.noteName);
      if (item) node.textContent = item.displayName;
    }
    const articles = [];
    const seen = new Set();
    for (const theme of config.notes) {
      for (const article of current.get(theme.url)?.articles || []) {
        if (!seen.has(article.url)) { articles.push({...article,category:theme.category}); seen.add(article.url); }
      }
    }
    articles.sort((a,b) => Date.parse(b.publishedAt) - Date.parse(a.publishedAt));
    if (articles.length) {
      const cards = articles.slice(0,6).map(article => {
        const card = element('a','article-card');
        card.href = article.url; card.target = '_blank'; card.rel = 'noopener noreferrer';
        const imageBox = element('div','article-image');
        try {
          const url = new URL(article.image);
          if (url.protocol !== 'https:' || url.hostname !== 'assets.st-note.com' || url.username || url.password || url.port) throw new Error();
          const img = element('img'); img.src = url.href; img.alt = ''; img.width = 640; img.height = 336; img.loading = 'lazy'; img.decoding = 'async'; img.referrerPolicy = 'no-referrer';
          img.addEventListener('error', () => img.remove(), {once:true}); imageBox.append(img);
        } catch { /* Thumbnail is optional; the article stays accessible. */ }
        const body = element('div','article-body'); const meta = element('p','article-meta');
        const time = element('time','',dateFormat.format(new Date(article.publishedAt)).replaceAll('/','.'));
        time.dateTime = article.publishedAt;
        meta.append(element('span','',article.category.split('・')[0]),time);
        const link = element('span','article-link','noteで読む '); const arrow=element('span','','↗');arrow.setAttribute('aria-hidden','true');link.append(arrow);
        body.append(meta,element('h3','',article.title),link); card.append(imageBox,body); return card;
      });
      document.getElementById('latest-articles').replaceChildren(...cards);
      document.getElementById('latest').hidden = false;
    }
    const fetched = [...current.values()].map(n=>Date.parse(n.fetchedAt)).filter(Number.isFinite);
    const oldest = fetched.length ? Math.min(...fetched) : 0;
    const stale = current.size < config.notes.length || [...current.values()].some(n=>n.status !== 'ok') || Date.now()-oldest > 48*60*60*1000;
    const updated = oldest ? `（取得：${dateFormat.format(new Date(oldest))}）` : '';
    if (status) status.textContent = `${stale || source !== 'remote' ? '保存済みの記事を表示しています。' : 'noteの公開RSSから取得した記事です。'}${updated} 最新の投稿は各noteでもご確認いただけます。`;
    try { localStorage.setItem(cacheKey,JSON.stringify({schemaVersion:1,notes:[...current.values()]})); } catch { /* Storage may be disabled. */ }
  }
  async function load() {
    let config;
    try { config = await json('/data/site.json'); if (!Array.isArray(config.notes)) return; } catch { return; }
    try { const saved = localStorage.getItem(cacheKey); if (saved) render(JSON.parse(saved),config,'browser'); } catch { /* Keep static snapshot. */ }
    try { render(await json('/data/notes.json'),config,'local'); } catch { /* Keep previous successful snapshot. */ }
    const remote = config.remoteDataUrl;
    if (typeof remote !== 'string' || !/^https:\/\/raw\.githubusercontent\.com\/[\w.-]+\/[\w.-]+\/[^\s]+\/data\/notes\.json$/.test(remote)) return;
    // Refresh the public CDN cache key every five minutes. A mutable branch URL
    // may otherwise keep serving the previous workflow's JSON despite no-cache.
    const refreshUrl = new URL(remote);
    refreshUrl.searchParams.set('v', String(Math.floor(Date.now() / 300000)));
    try { render(await json(refreshUrl.href),config,'remote'); }
    catch { if (status) status.textContent = '自動更新に接続できないため、保存済みの記事を表示しています。最新の投稿は各noteからご確認ください。'; }
  }
  document.querySelectorAll('.article-image img').forEach(img=>img.addEventListener('error',()=>img.remove(),{once:true}));
  if (location.protocol !== 'file:') load();
  const share = document.getElementById('share'); const shareStatus = document.getElementById('share-status');
  share?.addEventListener('click',async()=>{
    const url = document.querySelector('link[rel="canonical"]').href;
    const title = document.title;
    try {
      if (navigator.share) { await navigator.share({title,url}); shareStatus.textContent = '共有しました。'; }
      else if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(url); shareStatus.textContent = 'ページのURLをコピーしました。'; }
      else { shareStatus.replaceChildren(document.createTextNode('共有用URL：'),element('a','',url)); shareStatus.querySelector('a').href = url; }
    } catch (error) { if (error.name !== 'AbortError') shareStatus.textContent = `共有用URL：${url}`; }
  });
})();
