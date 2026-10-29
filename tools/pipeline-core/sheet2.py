import os,sys
from PIL import Image,ImageDraw
R=sys.argv[1]; out=sys.argv[2]
fs=sorted(f for f in os.listdir(R) if os.path.isfile(os.path.join(R,f))); W=380;H=330;cols=5
rows=(len(fs)+cols-1)//cols
S=Image.new("RGB",(cols*W,rows*H),(40,40,40)); d=ImageDraw.Draw(S)
for i,f in enumerate(fs):
    im=Image.open(os.path.join(R,f)).convert("RGBA"); sz=im.size; im.thumbnail((W-10,H-30))
    bg=Image.new("RGBA",im.size,(200,0,200,255)); bg.alpha_composite(im)
    x=(i%cols)*W;y=(i//cols)*H; S.paste(bg.convert("RGB"),(x+5,y+5)); d.text((x+5,y+H-20),f"{f} {sz}",fill=(255,255,255))
S.save(out)
