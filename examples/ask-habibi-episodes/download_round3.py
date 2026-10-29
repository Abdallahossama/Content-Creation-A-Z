"""Round-3 downloads, approved by the user 18 Oct 2026 (real photos, men only). Pexels CDN + Wikimedia API 1920px thumbs."""
import json, os, time, urllib.parse, urllib.request
UA = {"User-Agent": "AskHabibi-video/1.0 (small educational YouTube channel; one-off downloads)"}
M = "D:/why habibi/_media/"
PX = [("photos_thumbs/th_pyramids_cairo.jpg", 33629163), ("photos_thumbs/th_dunes.jpg", 16580387), ("photos_thumbs/th_glacier.jpg", 8318356),
      ("photos_thumbs/th_clothing_store.jpg", 19411621), ("photos_thumbs/th_fur.jpg", 5840852), ("photos_thumbs/th_shocked_man2.jpg", 8727506),
      ("photos_thumbs/th_pointing_man.jpg", 15835597), ("photos_thumbs/th_puzzled_man.jpg", 8638772),
      ("photos_ep07/f7_phone.jpg", 11934173), ("photos_ep07/f7_books.jpg", 7682364), ("photos_ep07/f7_button.jpg", 19667586),
      ("photos_ep08/f8_tv.jpg", 13279672), ("photos_ep08/f8_pool.jpg", 31591857), ("photos_ep08/f8_door.jpg", 8339246), ("photos_ep08/f8_eye_contact.jpg", 5938157),
      ("photos_ep08/f8_man_dog.jpg", 36826318), ("photos_ep08/f8_green_toy.jpg", 11958337), ("photos_ep08/f8_brows.jpg", 3655387)]
WM = [("photos_thumbs/th_pyramids_cairo_aerial.jpg", "File:Giza,_Dahshur_and_Saqqara_-_Giza8254.jpg"),
      ("photos_ep07/f7_tablet.jpg", "File:Cuneiform_tablet-_student_exercise_tablet_MET_DP360672.jpg"),
      ("photos_ep07/f7_rattle.jpg", "File:Terracotta_rattle_in_the_form_of_a_pig_MET_DP2031.jpg"),
      ("photos_ep07/f7_cave_animal.jpg", "File:Altamira,_bison,_museum.JPG"),
      ("photos_ep07/f7_bone_dice.jpg", "File:Musée_GR_de_Saint-Romain-en-Gal_27_07_2011_13_Des_et_jetons.jpg"),
      ("photos_ep08/f8_brain.jpg", "File:MRI_Image_of_Human_Head_(94-087-1).jpeg")]
def get(url, out):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read(); open(out, "wb").write(data); return len(data)
os.makedirs(M + "photos_thumbs", exist_ok=True)
for out, pid in PX:
    try: print(out, get(f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?cs=srgb&fm=jpg&w=2400", M + out), flush=True)
    except Exception as e: print("FAIL", out, e, flush=True)
    time.sleep(2)
for out, title in WM:
    try:
        q = urllib.parse.urlencode({"action": "query", "format": "json", "prop": "imageinfo", "iiprop": "url", "iiurlwidth": "1920", "titles": title})
        d = json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA), timeout=60))
        ii = list(d["query"]["pages"].values())[0]["imageinfo"][0]; time.sleep(4)
        print(out, get(ii.get("thumburl") or ii["url"], M + out), flush=True)
    except Exception as e: print("FAIL", out, e, flush=True)
    time.sleep(4)
print("ALLDONE")
