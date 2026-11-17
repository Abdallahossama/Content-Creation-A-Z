import sys, os
sys.path.insert(0, 'D:/the-bill-explained/tools')
from zimage import gen
OUT = 'D:/why habibi/_newchannel/_rethumb_nov17/bg/'
STYLE = ', cinematic still, photorealistic, gritty dark film grade, high contrast, deep shadows, 35mm film grain, dramatic lighting, no women'
JOBS = [
 ('alc_cell', 21, 'inside a 1960s prison cell at night, a papier-mache dummy head with painted face and real hair lying on a pillow in a narrow iron bed under a grey blanket, a guard flashlight beam on the head, bars in foreground, cold blue light'),
 ('fra_ships', 31, 'two 1840s wooden Royal Navy sailing ships with three masts trapped in thick Arctic pack ice, a line of exhausted men in long dark coats hauling a heavy wooden sledge across the ice toward the camera, blizzard, icy blue twilight'),
 ('fra_close', 32, 'close view of an 1840s wooden sailing ship frozen into pack ice, ice-coated rigging and masts, snow storm, a single lantern glowing on deck, icy blue and black'),
 ('coo_stairs', 41, 'night rainstorm, the rear airstair of a 1970s Boeing 727 jet lowered open in flight high above dark pine forest, rain streaks, red cabin light spilling out, view from behind and below the plane'),
 ('coo_forest', 42, 'dark Pacific Northwest fir forest at night in heavy rain, a torn white parachute canopy caught high in the trees, flashlight beams of search party men in 1970s raincoats below, fog'),
 ('roa_fort', 51, 'abandoned 1580s English colonial settlement inside a wooden palisade on a misty coastal island forest at sunset, empty thatched cottages, overgrown, an old sailing ship anchored offshore, golden orange sky, eerie'),
 ('roa_tree', 52, 'close up of the trunk of an old oak tree with weathered bark and a large smooth stripped flat area of pale wood in the centre, misty forest behind, warm sunset light, shallow depth of field'),
 ('and_balloon', 61, 'a collapsed hydrogen balloon wreck lying on Arctic pack ice in 1897, torn grey fabric and netting, wicker basket, three men in 1890s wool clothing and caps pulling a loaded wooden sledge away across the ice, grey overcast, cold'),
 ('alc_boat2', 12, 'Alcatraz island prison at night from water level, thick fog, a powerful searchlight sweeping the black water, choppy cold waves, a lone wooden paddle floating in the foreground'),
]
for name, seed, p in JOBS:
    out = OUT + name + '.png'
    if os.path.exists(out): continue
    gen(p + STYLE, out, 1344, 768, seed=seed)
