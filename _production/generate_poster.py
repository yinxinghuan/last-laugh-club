#!/usr/bin/env python3
"""Generate and finish the formal Aigram poster for Last Laugh Club."""
from __future__ import annotations
import json,time,urllib.request
from io import BytesIO
from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance,ImageFont

ROOT=Path(__file__).resolve().parents[1]
API='https://chat.aiwaves.tech/aigram/api/gen-image'
REF='https://cdn.aiwaves.tech/prod/telegram/avatar/0/1785575267265826.webp'
RAW=ROOT/'_production'/'poster-source.webp'
OUT=ROOT/'public'/'poster.png'
THUMB=ROOT/'_qa'/'ui'/'poster-160.png'
PROVENANCE=ROOT/'_production'/'poster-provenance.json'
FONT='/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf'
PROMPT=(
 'Create premium square cinematic anthology key art, one unified live-action composition, not a collage and not a screenshot. '
 'Three underestimated Western protagonists stand shoulder to shoulder in a dark theatrical space and look newly confident. '
 'At frame left Elena is a Western Afro-Latina waitress age 29 with dark hair in a low bun and a fitted burgundy service jacket; '
 'she raises one dark metal serving tray with exactly one bright silver engagement ring at its center. At center Mara is a Western '
 'Black seamstress age 27 with short natural curls wearing the same luminous cobalt-blue gown covered in water-activated violet, '
 'silver and turquoise flowers; camera flashes behind her turn into a halo. At frame right Luis is a Western Latino father age 56 '
 'with salt-and-pepper hair and a modest worn navy suit; he holds one open antique walnut music box close to his heart. Behind each '
 'hero, elegant crowd silhouettes and phone cameras pivot away from accusation toward recognition. One thin tomato-red horizontal '
 'judgment beam enters from the left, breaks into three fragments behind their shoulders, and becomes warm cream light in front. '
 'Deep black negative space, cream highlights, burgundy, cobalt and walnut palette, realistic faces and fabric, dramatic 35mm '
 'lighting, powerful but emotionally human. Exactly three foreground adults, one tray, one ring and one music box. Leave the upper '
 '25 percent calm deep black with low detail for later title typography. Keep all faces and evidence objects inside the central 72 '
 'percent and above the bottom 20 percent. Readable at 160 pixels. No text, no letters, no numbers, no logo, no UI, no watermark, '
 'no East Asian styling, no duplicate person, no extra hand, no duplicate ring, no duplicate music box.'
)

def request_image():
 payload=json.dumps({'prompt':PROMPT,'ref_url':REF}).encode()
 for attempt,delay in enumerate((0,3,8,15)):
  if delay:time.sleep(delay)
  req=urllib.request.Request(API,data=payload,method='POST',headers={'Content-Type':'application/json','Origin':'https://aigram.app','User-Agent':'Mozilla/5.0'})
  try:
   with urllib.request.urlopen(req,timeout=900) as response: result=json.loads(response.read())
   url=result.get('url')
   if not url:raise RuntimeError(result)
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=300) as response:data=response.read()
   RAW.write_bytes(data)
   return url
  except Exception:
   if attempt==3:raise

def font_fit(text,max_width,start):
 for size in range(start,47,-2):
  font=ImageFont.truetype(FONT,size)
  if font.getbbox(text)[2]<=max_width:return font
 return ImageFont.truetype(FONT,48)

def main():
 url=request_image() if not RAW.exists() else 'reused-local-aigram-source'
 image=Image.open(BytesIO(RAW.read_bytes())).convert('RGB').resize((1024,1024),Image.Resampling.LANCZOS)
 image=ImageEnhance.Contrast(image).enhance(1.06)
 shade=Image.new('RGBA',(1024,1024),(0,0,0,0));px=shade.load()
 for y in range(258):
  a=255
  for x in range(1024):px[x,y]=(4,4,4,a)
 image=Image.alpha_composite(image.convert('RGBA'),shade);draw=ImageDraw.Draw(image)
 lines=[('LAST',18,(240,68,56,255),188),('LAUGH CLUB',144,(247,239,223,255),148)]
 for text,y,color,size in lines:
  font=font_fit(text,880,size);box=draw.textbbox((0,0),text,font=font,stroke_width=2);x=(1024-(box[2]-box[0]))//2
  draw.text((x+4,y+8),text,font=font,fill=(0,0,0,160),stroke_width=2)
  draw.text((x,y),text,font=font,fill=color,stroke_width=2,stroke_fill=(5,5,5,235))
 OUT.parent.mkdir(parents=True,exist_ok=True);THUMB.parent.mkdir(parents=True,exist_ok=True)
 image.convert('RGB').save(OUT,'PNG',optimize=True)
 image.convert('RGB').resize((160,160),Image.Resampling.LANCZOS).save(THUMB,'PNG',optimize=True)
 PROVENANCE.write_text(json.dumps({'generator':'Aigram transit gen-image','endpoint':API,'origin':'https://aigram.app','url':url,'ref_url':REF,'prompt':PROMPT,'finishing':'Pillow contrast, title gradient, English raster typography','output':'public/poster.png'},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
