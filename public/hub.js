(() => {
 'use strict';
 document.documentElement.classList.add('js');
 const button=document.getElementById('menu-toggle'),nav=document.getElementById('main-nav');
 const close=()=>{nav?.classList.remove('is-open');button?.setAttribute('aria-expanded','false');};
 button?.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
 nav?.addEventListener('click',e=>{if(e.target.closest('a'))close();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&button?.getAttribute('aria-expanded')==='true'){close();button.focus();}});
 // If JavaScript or the observer fails, all content remains visible.
 if('IntersectionObserver'in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){const nodes=document.querySelectorAll('.guide-teasers>a,.future-tool');if(nodes.length){const ob=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting){entry.target.classList.add('is-visible');ob.unobserve(entry.target);}},{threshold:.05});for(const node of nodes){node.dataset.reveal='';ob.observe(node);}document.documentElement.classList.add('reveal-ready');}}
})();
