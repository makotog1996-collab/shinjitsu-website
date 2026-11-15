(() => {
 'use strict';
 if(location.protocol!=='https:'||location.hostname!=='neon-empanada-519607.netlify.app')return;
 const allowed=new Set(['tool_start','tool_complete','tool_save','tool_copy','tool_export']);
 window.addEventListener('makoto:tool',event=>{const d=event.detail;if(!d||!allowed.has(d.operation)||typeof window.gtag!=='function')return;const data={tool_id:'repurpose',transport_type:'beacon'};if(['x','tiktok','pinterest','note'].includes(d.channel))data.channel=d.channel;if(['md','csv','json'].includes(d.format))data.format=d.format;window.gtag('event',d.operation,data);});
})();
