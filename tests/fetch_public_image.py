"""Forward only public note thumbnails using Python's verified HTTPS transport.
For browser QA in environments whose Chromium does not trust the proxy CA.
Never used by the deployed website; no TLS verification is disabled.
"""
import hashlib,json,sys,urllib.request
from pathlib import Path
from urllib.parse import urlsplit
u=sys.argv[1];p=urlsplit(u)
if p.scheme!='https' or p.hostname!='assets.st-note.com' or p.username or p.password:raise ValueError('Only the public note thumbnail host is allowed')
cache=Path(__file__).resolve().parents[1]/'test-results/renewal/image-cache';cache.mkdir(parents=True,exist_ok=True);file=cache/(hashlib.sha256(u.encode()).hexdigest()+'.jpg')
if not file.exists():
 response=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=25)
 if response.status!=200 or not response.headers.get('Content-Type','').startswith('image/'):raise ValueError('Not a successful image response')
 data=response.read(5000001)
 if len(data)>5000000:raise ValueError('Image too large')
 file.write_bytes(data)
head=file.read_bytes()[:12]
kind='image/png' if head.startswith(b'\x89PNG') else ('image/webp' if head.startswith(b'RIFF') and head[8:12]==b'WEBP' else 'image/jpeg')
print(json.dumps({'path':str(file),'contentType':kind,'verifiedHTTPS':True}))
