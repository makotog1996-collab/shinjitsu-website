"""One small catalog for available and planned tools; static, no runtime API."""
import html,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def esc(x):return html.escape(str(x),quote=True)
def render_tools():
 available=[];planned=[]
 for item in json.loads((ROOT/'config/tools.json').read_text()):
  if not re.fullmatch(r'[a-z0-9-]{1,60}',item['id']):raise ValueError('Invalid tool id')
  if item['status']=='available':
   url=item['url']
   if not re.fullmatch(r'/tools/[a-z0-9-]+/',url) or not (ROOT/'public'/url.strip('/')/'index.html').is_file():raise ValueError('Missing local tool')
   features=''.join('<li>'+esc(x)+'</li>'for x in item['features'])
   visual='<div class="tool-visual" aria-hidden="true"><div class="visual-source"><small>YOUR ORIGINAL</small><b>記事の要点</b><i></i><i></i><i></i></div><div class="visual-targets"><span><b>X</b><small>ひとつの気づき</small></span><span><b>TikTok</b><small>短い構成メモ</small></span><span><b>Pinterest</b><small>保存する理由</small></span><span><b>note</b><small>記事への入口</small></span></div></div>'
   available.append('<article class="tool-feature"><div class="tool-copy"><div class="tool-topline"><span class="available-badge">利用できます</span><span>'+esc(item['label'])+'</span></div><h3>'+esc(item['name'])+'</h3><p>'+esc(item['description'])+'</p><ul class="tool-feature-list">'+features+'</ul><a class="primary-button" href="'+esc(url)+'" data-tool-id="'+esc(item['id'])+'">無料で下書きを整理する <span aria-hidden="true">↗</span></a></div>'+visual+'</article>')
  elif item['status']=='planned':
   planned.append('<article class="future-tool"><span class="future-icon" aria-hidden="true">'+('▧'if item['id']=='image-check'else'“')+'</span><div><h4>'+esc(item['name'])+'</h4><p>'+esc(item['description'])+'</p></div><span class="planned-badge">検討中</span></article>')
  else:raise ValueError('Invalid tool status')
 return {'TOOL_CARDS':''.join(available),'PLANNED_TOOLS':''.join(planned)}
