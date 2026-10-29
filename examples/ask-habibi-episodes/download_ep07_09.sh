#!/bin/sh
# approved by the user 18 Oct 2026 (photo_candidates_ep07-09.md). Pexels via CDN, Wikimedia via the API's 1920 px thumburl.
UA="AskHabibi-video/1.0 (small educational YouTube channel; one-off downloads)"
D7="D:/why habibi/_media/photos_ep07"; D8="D:/why habibi/_media/photos_ep08"; D9="D:/why habibi/_media/photos_ep09"; mkdir -p "$D7" "$D8" "$D9"
px() { sleep 2; curl -sL -A "$UA" --max-time 180 -o "$1" "https://images.pexels.com/photos/$2/pexels-photo-$2.jpeg?cs=srgb&fm=jpg&w=2400"; printf "%-44s %s\n" "$1" "$(file -b "$1" | cut -c1-20)"; }
wm() { u=$(curl -s -A "$UA" "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&iiurlwidth=1920&titles=File:$2" | PYTHONUTF8=1 uv run --no-project python -c "import json,sys; p=list(json.load(sys.stdin)['query']['pages'].values())[0]['imageinfo'][0]; print(p.get('thumburl') or p['url'])"); sleep 5; curl -sL -A "$UA" --max-time 180 -o "$1" "$u"; printf "%-44s %s\n" "$1" "$(file -b "$1" | cut -c1-20)"; }
wm "$D7/f7_ur_board.jpg" "British_Museum_Royal_Game_of_Ur.jpg"
wm "$D7/f7_senet_box.jpg" "Game_Box_for_Playing_Senet_and_Twenty_Squares_MET_DP116121.jpg"
wm "$D7/f7_nefertari_senet.jpg" "Queen_Nefertari_Playing_Senet_MET_DT11770.jpg"
wm "$D7/f7_beni_hasan.jpg" "Beni_Hasan._Tombe_van_Baqet_III_Muurschildering_Twee_worstelaars_(facsimile),_GD005162.jpg"
wm "$D7/f7_bone_flute.jpg" "Flöte_aus_der_Steinzeit.jpg"
wm "$D7/f7_divje_babe.jpg" "Divje_Babe_flute_in_the_National_Museum_of_Slovenia_01.jpg"
px "$D7/f7_hands.jpg" 37054079
wm "$D7/f7_flutings.jpg" "Neanderthal_finger_flutings_(cropped).jpg"
wm "$D7/f7_knucklebones.jpg" "Group_of_eight_glass_astragali_(knucklebones)_MET_DP121111.jpg"
wm "$D7/f7_olympia.jpg" "Ancient_Olympic_Stadium_Entrance_(5987161338).jpg"
wm "$D7/f7_bull_leap.jpg" "Bull_leaping_minoan_fresco_archmus_Heraklion_(cropped).jpg"
wm "$D7/f7_pompeii_graffiti.jpg" "House_of_the_Vettii_VI_15,1_Pompeii_2017_Graffiti_on_left_hand_wall_of_vestibule_courtesy_of_Buzz_Ferebee.jpg"
px "$D7/f7_pompeii_street.jpg" 36366052
px "$D7/f7_ballcourt.jpg" 28278494
wm "$D7/f7_dolls.jpg" "Roman_Bone_Dolls,_275-300_AD_(10457011886).jpg"
wm "$D7/f7_banquet.jpg" "Banquet_Scene_with_Musicians,_Tomb_of_Nakht_MET_LC-15_5_19j-k_EGDP028769.jpg"
wm "$D7/f7_mancala.jpg" "Mancala_board_at_an_Ezidi_home_in_June_of_2019_in_Wardia_village_near_Shingal_town_01.jpg"
px "$D8/f8_dog_eyes.jpg" 17525525
px "$D8/f8_red_ball.jpg" 11908217
px "$D8/f8_park_dog.jpg" 5981109
px "$D8/f8_nose.jpg" 1188575
px "$D8/f8_greeting.jpg" 4422100
px "$D8/f8_puppy_eyes.jpg" 33182938
px "$D8/f8_face.jpg" 36763373
px "$D8/f8_shoes.jpg" 16659409
px "$D8/f8_police.jpg" 30487150
px "$D8/f8_wolf.jpg" 31767241
px "$D9/f9_park.jpg" 37590863
px "$D9/f9_seniors.jpg" 12013184
px "$D9/f9_evening.jpg" 19996082
px "$D9/f9_traffic.jpg" 15983056
px "$D9/f9_leafy.jpg" 15395828
px "$D9/f9_feet.jpg" 7880267
px "$D9/f9_steps.jpg" 1428005
px "$D9/f9_desk.jpg" 36713392
px "$D9/f9_stride.jpg" 9486646
wm "$D9/f9_gray_heart.png" "Gray490.png"
wm "$D9/f9_gray_lungs.png" "Gray970.png"
wm "$D9/f9_gray_hippocampus.png" "Gray739-emphasizing-hippocampus.png"
wm "$D9/f9_gray_stomach.png" "Gray1050.png"
wm "$D9/f9_gray_knee.png" "Gray347.png"
wm "$D9/f9_gray_lymph.png" "Gray599.png"
wm "$D9/f9_pedometer.jpg" "Pedometer_K+R.jpg"
echo ALLDONE
