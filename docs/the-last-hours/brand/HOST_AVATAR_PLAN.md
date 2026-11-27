# The Last Hours: host avatar ("The File Keeper", with your face). Owner request, 27 Nov 2026

## What Omar Qany does (studied over the whole 49-min GTA video, storyboard frames every ~3.5 s)
- ONE character = the brand: his own face as a semi-realistic illustrated head, always wearing the same signature prop
  (Luffy's straw hat). Floating head, no body, clean cut-out, centred on the channel's dark purple grid background.
- That head is his on-screen host. It pops in every ~1-2 min, whenever he gives his own opinion or a joke ("honestly",
  "Damn you, Sony"), so the "friend" voice has a face. Around 25 appearances in 50 min.
- The same character is everywhere: the thumbnail hero (head in the middle, holding a revolver, the 5 GTA heroes around
  him), the corner logo bug (always on, top-left), the end screen (thumbnail art + animated SUBSCRIBE button + a thumbs-up).
- Result: you remember the CHANNEL, not just the video. Ours today is a faceless noir file. The fix is the same move.

## Our version (keeps the noir "File Keeper" brand, not a copy of his hat)
- Your face, semi-realistic illustrated, wearing a black 1940s detective FEDORA with a deep-red band (our red #B22222),
  dark trench-coat collar turned up. The fedora is our "straw hat": the one prop people remember.
- Uses: (1) pop-in head for every friend aside in the scripts (Vice City has ~25); (2) thumbnail hero holding a case file /
  flashlight; (3) corner bug; (4) end screen with SUBSCRIBE; (5) channel avatar + banner.
- Rules kept: real people in stories still come only from real photos; the avatar is only the host.

## Step 1 (you, ChatGPT, free): attach the photo, paste PROMPT 1, then PROMPT 2 in the same chat. Send me every PNG.
Best results: also attach a straight-on face photo with good light (no sunglasses), if you have one.

### PROMPT 1 (master head)
Using the attached photos of me, create my channel mascot: a semi-realistic digital painting of MY head and neck only
(keep my exact face: eye shape, nose, beard shape and density, hairline, skin tone, so friends would recognise me).
I am wearing a black 1940s detective fedora with a deep red band, tilted slightly, and the turned-up collar of a dark
charcoal trench coat. Calm, confident, slightly amused expression, looking at the camera. Clean crisp edges, soft
cinematic rim light in red from the left and cold blue from the right, rich contrast, premium YouTube-mascot quality,
like a polished character portrait. Centred, head fills 80% of a square 2048x2048 canvas, plain flat light-grey background
(I will cut it out), no text, no logo, no hands.

### PROMPT 2 (expressions, same character, same hat and coat, same framing, one image each)
Keep the exact same character, hat, coat, lighting and framing as the previous image. Make 6 separate images:
1. eyebrows raised, shocked, mouth slightly open
2. smirking, one eyebrow up, sceptical
3. thinking, eyes up to the side
4. serious, narrowed eyes, investigating
5. laughing, eyes half closed
6. disappointed, slight frown, shaking head

### PROMPT 3 (thumbnail hero, half body)
Same character, waist up, holding an old manila case file stamped "CLASSIFIED" in red in one hand and a lit flashlight in
the other, looking straight at camera, dramatic noir lighting, plain light-grey background, no other text, 2048x2048.

## Step 2 (me, free, local)
Cut out every PNG (rembg), grade to the channel look, and build:
- `host_pop()` for lastkit renders: the head slides/pops in at a corner with a small bounce + soft shadow on each aside
  line (script marks: lines starting with "Honestly", "Okay", "Imagine that", "Quick gamer note", "Spoiler", "Look,"),
  expression picked per line (shock / smirk / thinking...).
- thumbnail template: avatar hero centre + scene + 2-4 words + date block.
- end screen: thumbnail art + SUBSCRIBE button animation + thumbs-up, and the corner bug.
- Then: new channel avatar + banner, and a sheet for your OK before anything goes live.
