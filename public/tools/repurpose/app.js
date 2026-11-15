'use strict';
(() => {
const $ = id => document.getElementById(id);
const channels=['x','tiktok','pinterest','note'];
const labels={x:'X / 投稿の下書き',tiktok:'TikTok / 約25秒の構成メモ',pinterest:'Pinterest / タイトル・説明・画像企画',note:'note / 記事へ案内する紹介文'};
const tips={x:'文字数は目安です。URLの扱いや投稿上限は、投稿画面で確認してください。',tiktok:'秒数は構成の目安です。自分の声で読み、尺を調整してください。説明欄のURLがクリックできるとは限りません。',pinterest:'画像案は制作指示のメモです。画像は生成していません。タイトル・説明・リンクは投稿画面で分けて設定してください。',note:'紹介文の型です。他人の記事の転載・二重投稿を勧めるものではありません。元記事との役割を分けてください。'};
const themeNames={ai:'AI・テクノロジー',conversation:'会話・人間関係',habit:'自分磨き・習慣',life:'暮らし・時短'};
const CHECKS=['rights','facts','pr','channel'];
const STORAGE='makoto-repurpose-v1';
const track=(operation,extra={})=>window.dispatchEvent(new CustomEvent('makoto:tool',{detail:{operation,...extra}}));
let started=false;
$('source-form').addEventListener('input',()=>{if(!started){started=true;track('tool_start');}});
const sample={title:'朝の支度をラクにする、小さな準備',audience:'朝の支度でいつも慌てる人',points:'前の晩に持ち物を一か所へ置く\n翌朝の服をひと組だけ選んでおく\n出発時刻の10分前に片づけを始める',theme:'life',goal:'try',url:'',campaign:'article_reuse'};
let current=null,active='x',library=[],persisted=true;
const status=message=>{$('status').textContent=message;};
const safeURL=(text)=>{
 if(!text.trim())return '';
 const u=new URL(text.trim());
 if(!['http:','https:'].includes(u.protocol)||u.username||u.password)throw new Error('URLは認証情報を含まないhttp / httpsにしてください。');
 return u.href;
};
function utm(raw,channel,campaign){if(!raw)return '';const u=new URL(raw);u.searchParams.set('utm_source',channel);u.searchParams.set('utm_medium',channel==='note'?'referral':'social');u.searchParams.set('utm_campaign',campaign);return u.href;}
function inputData(){
 const data={};for(const key of Object.keys(sample))data[key]=$(key).value.trim();
 if(!data.title||!data.audience)throw new Error('タイトルと届けたい相手を入力してください。');
 const points=data.points.split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
 if(points.length!==3||points.some(p=>p.length>120))throw new Error('要点をちょうど3行、1行1〜120文字で入力してください。');
 data.points=points.join('\n');data.url=safeURL(data.url);
 if(!/^[a-zA-Z0-9_-]{1,40}$/.test(data.campaign))throw new Error('計測ラベルは英数字・_・-で1〜40文字にしてください。');
 return data;
}
function populate(data){for(const key of Object.keys(sample))$(key).value=data[key];}
function compose(data){
 const [a,b,c]=data.points.split('\n');
 const action={try:'できそうなものを、ひとつ試してみてください。',read:'手順と考え方は、元の記事で紹介しています。',save:'次に必要になったときのために、メモしておきませんか。'}[data.goal];
 const links=Object.fromEntries(channels.map(channel=>[channel,utm(data.url,channel,data.campaign)]));
 const tail=channel=>links[channel]?'\n\n元の記事\n'+links[channel]:'';
 return {
 x:`${data.audience}へ。\n\n${a}。\n\n${action}${tail('x')}`,
 tiktok:`【構成メモ：${data.title}】\n\n0〜3秒｜問いかけ\n「${data.audience}へ。こんな準備はどうでしょう？」\n\n3〜15秒｜手元や実演を3カット\n① ${a}\n② ${b}\n③ ${c}\n\n15〜25秒｜自分の言葉でまとめる\n${action}\n\n撮影メモ：自分の手元・道具だけで構成。数字や効果を足す場合は根拠を確認。\n説明欄の案内：${data.title}${tail('tiktok')}`,
 pinterest:`【タイトル案】\n${data.title}\n\n【説明案】\n${data.audience}に向けた、${themeNames[data.theme]}のメモ。\n・${a}\n・${b}\n・${c}\n${action}\n\n【自分で作る画像の案】\n縦長の1枚。上部に記事の短い見出し、中央に3つの要点、下部に自分の発信名。読みやすい余白を残し、画像・フォントの利用条件も確認する。${tail('pinterest')}`,
 note:`${data.audience}に向けて、記事を書きました。\n\n「${data.title}」\n\n今回整理したのは、この3つです。\n・${a}\n・${b}\n・${c}\n\n${action}${tail('note')}\n\n※紹介文の下書きです。自分の実例や背景を加え、元記事との役割を調整してください。`
 };
}
function syncDraft(){if(current)current.outputs[active]=$('draft').value;updateCount();}
function updateCount(){$('count').textContent=Array.from($('draft').value).length+'文字（概算）';}
function render(){
 document.querySelectorAll('[data-channel]').forEach(button=>{const yes=button.dataset.channel===active;button.setAttribute('aria-selected',String(yes));button.tabIndex=yes?0:-1;});
 $('channel-panel').setAttribute('aria-labelledby','tab-'+active);$('channel-label').textContent=labels[active];$('channel-tip').textContent=tips[active];
 $('draft').value=current?current.outputs[active]:'';$('posted').checked=current?Boolean(current.posted[active]):false;
 ['draft','copy','posted','save','export'].forEach(id=>$(id).disabled=!current);
 $('output-meta').textContent=current?`${themeNames[current.input.theme]} / 4媒体の型を整理しました。出力は編集できます。`:'サンプルを読み込み、整理ボタンから始められます。';
 document.querySelectorAll('[data-check]').forEach(el=>el.checked=Boolean(current&&current.checks[el.dataset.check]));updateReview();updateCount();
}
function updateReview(){const n=[...document.querySelectorAll('[data-check]')].filter(el=>el.checked).length;$('review-status').textContent=`確認 ${n} / 4${n===4?' — 最後は投稿画面でも確認を。':''}`;}
function store(){try{localStorage.setItem(STORAGE,JSON.stringify(library));persisted=true;}catch(e){persisted=false;}return persisted;}
function validateDocument(value){
 if(!value||value.version!==1||!value.input||!value.outputs)throw new Error('このツールのJSONファイルではありません。');
 const data={};const max={title:120,audience:80,points:900,url:2000,campaign:40,theme:30,goal:30};
 for(const key of Object.keys(sample)){if(typeof value.input[key]!=='string'||value.input[key].length>max[key])throw new Error('入力データの形式・長さが不正です。');data[key]=value.input[key];}
 if(!data.title.trim()||!data.audience.trim()||!themeNames[data.theme]||!['try','read','save'].includes(data.goal)||!/^[a-zA-Z0-9_-]{1,40}$/.test(data.campaign))throw new Error('入力データの値が不正です。');
 const ps=data.points.split('\n');if(ps.length!==3||ps.some(p=>!p.trim()||p.length>120))throw new Error('要点の形式が不正です。');data.url=safeURL(data.url);
 const out={},posted={},checks={};for(const channel of channels){if(typeof value.outputs[channel]!=='string'||value.outputs[channel].length>15000)throw new Error('出力データの形式・長さが不正です。');out[channel]=value.outputs[channel];posted[channel]=value.posted?.[channel]===true;}
 for(const key of CHECKS)checks[key]=value.checks?.[key]===true;
 return {version:1,id:typeof value.id==='string'&&/^[a-zA-Z0-9_-]{1,80}$/.test(value.id)?value.id:newId(),updated:typeof value.updated==='string'&&!Number.isNaN(Date.parse(value.updated))?new Date(value.updated).toISOString():new Date().toISOString(),input:data,outputs:out,posted,checks};
}
function newId(){return 'draft-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2,8);}
function renderLibrary(){
 const root=$('saved-list');root.replaceChildren();
 if(!library.length){const empty=document.createElement('div');empty.className='empty-state';empty.textContent='まだ保存した下書きはありません。整理して「端末に下書きを保存」から残せます。';root.append(empty);return;}
 library.forEach(item=>{
 const card=document.createElement('article');card.className='saved-card';const h=document.createElement('h3');h.textContent=item.input.title;const p=document.createElement('p');p.textContent=`${new Date(item.updated).toLocaleString('ja-JP')} · 投稿メモ ${channels.filter(ch=>item.posted[ch]).length}/4`;
 const actions=document.createElement('div');actions.className='saved-actions';
 const open=document.createElement('button');open.className='secondary';open.textContent='続きを開く';open.setAttribute('aria-label',item.input.title+' の続きを開く');open.onclick=()=>{current=structuredClone(item);populate(current.input);active='x';render();status('保存した下書きを開きました。入力の変更は整理し直すまで出力に反映されません。');$('workspace').scrollIntoView({behavior:'smooth'});};
 const remove=document.createElement('button');remove.className='text-button';remove.textContent='削除';remove.setAttribute('aria-label',item.input.title+' を削除');remove.onclick=()=>{library=library.filter(x=>x.id!==item.id);const ok=store();renderLibrary();status(ok?'この端末の保存一覧から削除しました。編集中・ダウンロード済みの控えは残ります。':'この画面の一覧から削除しました。端末保存へ反映できませんでした。');};
 actions.append(open,remove);card.append(h,p,actions);root.append(card);
 });
}
function activeDirty(){if(!current)return false;return Object.keys(sample).some(key=>$(key).value.trim()!==current.input[key]);}
$('source-form').addEventListener('submit',e=>{e.preventDefault();if(!started){started=true;track('tool_start');}$('form-error').textContent='';try{const data=inputData();current={version:1,id:newId(),updated:new Date().toISOString(),input:data,outputs:compose(data),posted:{},checks:{}};active='x';render();status('4媒体の型に整理しました。編集・確認してから、保存や持ち出しへ。');track('tool_complete');}catch(error){$('form-error').textContent=error.message;}});
$('draft').addEventListener('input',syncDraft);
$('posted').addEventListener('change',()=>{if(current)current.posted[active]=$('posted').checked;});
for(const el of document.querySelectorAll('[data-check]'))el.addEventListener('change',()=>{if(current)current.checks[el.dataset.check]=el.checked;updateReview();});
const tabs=[...document.querySelectorAll('[data-channel]')];
tabs.forEach((el,index)=>{el.addEventListener('click',()=>{syncDraft();active=el.dataset.channel;render();});el.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(index+1)%4;else if(e.key==='ArrowLeft')next=(index+3)%4;else if(e.key==='Home')next=0;else if(e.key==='End')next=3;else return;e.preventDefault();tabs[next].click();tabs[next].focus();});});
$('demo').onclick=()=>{populate(sample);$('form-error').textContent='';status('入力欄にサンプルを入れました。「4媒体の下書きを整理」で出力できます。現在の出力はそのままです。');};
$('copy').onclick=async()=>{if(!current)return;syncDraft();try{await navigator.clipboard.writeText(current.outputs[active]);track('tool_copy',{channel:active});status(labels[active].split(' /')[0]+'の編集中の下書きをコピーしました。');}catch(e){$('draft').focus();$('draft').select();status('自動コピーできませんでした。選択中の文章をCtrl+C（スマホはコピー操作）でコピーしてください。');}};
$('save').onclick=()=>{if(!current)return;syncDraft();if(activeDirty()){status('元の入力が変わっています。整理し直すか、入力を戻してから保存してください。出力の編集内容はそのまま残っています。');return;}if(channels.some(ch=>current.outputs[ch].length>15000)){status('保存する出力は1媒体15,000文字以内にしてください。');return;}current.updated=new Date().toISOString();library=[structuredClone(current),...library.filter(x=>x.id!==current.id)].slice(0,20);const ok=store();renderLibrary();if(ok)track('tool_save');status(ok?'このブラウザに保存しました。別端末用にはJSONで持ち出せます。':'端末保存が使えません。この画面内だけ保持しています。JSONで持ち出してください。');};
const csvCell=value=>'"'+(/^[\s]*[=+@-]/.test(value)?"'":'')+value.replace(/"/g,'""')+'"';
$('export').onclick=()=>{if(!current)return;syncDraft();if(activeDirty()){status('元の入力が変わっています。整理し直すか入力を戻してから持ち出してください。');return;}const format=$('format').value;let content,mime;
 if(format==='json'){content=JSON.stringify(current,null,2);mime='application/json';}
 else if(format==='csv'){content='\uFEFF'+[['media','title','draft','manually_posted'],...channels.map(ch=>[ch,current.input.title,current.outputs[ch],String(Boolean(current.posted[ch]))])].map(row=>row.map(csvCell).join(',')).join('\r\n');mime='text/csv';}
 else {content=`# ${current.input.title}\n\n作成：投稿リパーパス設計室\nこれは下書きです。公開前に事実・権利・各媒体の規約を確認してください。\n\n`+channels.map(ch=>`## ${labels[ch]}\n\n${current.outputs[ch]}\n\n手動投稿メモ：${current.posted[ch]?'投稿済み':'未投稿'}\n`).join('\n')+'\n## 確認記録\n'+CHECKS.map(k=>`- [${current.checks[k]?'x':' '}] ${k}`).join('\n');mime='text/markdown';}
 const blob=new Blob([content],{type:mime+';charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='makoto-drafts.'+format;document.body.append(a);a.click();a.remove();track('tool_export',{format});setTimeout(()=>URL.revokeObjectURL(url),1000);status(`${format.toUpperCase()}ファイルを書き出しました。ブラウザのダウンロード先を確認してください。`);
};
$('import').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{if(file.size>400000)throw new Error('JSONは400KB以内にしてください。');current=validateDocument(JSON.parse(await file.text()));populate(current.input);active='x';render();status('JSONから編集中の下書きを復元しました。端末にも残すには「保存」を押してください。');$('workspace').scrollIntoView({behavior:'smooth'});}catch(error){status('復元できませんでした：'+error.message);}e.target.value='';};
try{const saved=JSON.parse(localStorage.getItem(STORAGE)||'[]');if(!Array.isArray(saved))throw new Error();library=saved.slice(0,20).map(validateDocument);}catch(e){library=[];persisted=false;}
populate(sample);render();renderLibrary();if(!persisted)status('端末保存データを読めませんでした。JSONで持ち出せます。保存操作後に保存可否を表示します。');
})();
