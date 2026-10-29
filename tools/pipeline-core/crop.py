from PIL import Image,ImageDraw,ImageFont
R="D:/why habibi/1st video/claude_memes/raw/"; O="D:/why habibi/1st video/claude_memes/"
FONT="C:/Users/ossam/AppData/Local/CapCut/User Data/Cache/effect/7148699606082130433/9b03aa8db4f8d431e15f1660108d512b/Rubik-Bold.ttf"
def c(n,box,out=None,ext="jpg"):
    im=Image.open(R+n).convert("RGB")
    if box: im=im.crop(box)
    im.save(O+(out or n.rsplit('.',1)[0])+".png"); print(out or n, im.size); return im
# gru: top-left panel, write on board
im=Image.open(R+"grus_plan.jpg").convert("RGB").crop((0,0,350,224)).resize((1050,672),Image.LANCZOS)
d=ImageDraw.Draw(im)
f=ImageFont.truetype(FONT,78); f2=ImageFont.truetype(FONT,40)
# board approx x 615-1035 y 30-645 after 3x
cx=825
for txt,fnt,y,col in [("4",ImageFont.truetype(FONT,200),150,(30,40,110)),("LEVELS",f,380,(30,40,110)),("of 3AM",f2,490,(200,60,60))]:
    w=d.textlength(txt,font=fnt); d.text((cx-w/2,y),txt,font=fnt,fill=col)
im.save(O+"grus_plan_4levels.png"); print("gru",im.size)
c("harold.jpg",(0,300,480,601),"harold_smile")
c("monkey_puppet.jpg",(0,282,923,768),"monkey_puppet")
c("pawn_stars.jpg",None,"pawn_stars")
c("sad_pablo.jpg",(0,0,720,352),"sad_pablo")
c("scientist_myself.jpg",None,"scientist_myself")
c("sleeping_shaq.jpg",(306,0,640,316),"sleeping_shaq")
c("squidward_window.jpg",None,"squidward_window")
c("surprised_pikachu.jpg",(0,770,1893,1892),"surprised_pikachu")
c("this_is_fine.jpg",(291,0,580,282),"this_is_fine")
c("waiting_skeleton.jpg",None,"waiting_skeleton")
c("laughing_leo.png",None,"laughing_leo")
c("leo_cheers.jpg",None,"leo_cheers")
c("megamind_peeking.png",None,"megamind_peeking")
