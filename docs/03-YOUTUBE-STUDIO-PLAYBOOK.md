# YouTube Studio playbook (browser automation: Claude in Chrome)

Work in **your own new tab**; never navigate or force-navigate a tab the owner uses (uploads may be running: a "Leave site?" dialog
means an upload is in progress). Close your tabs when done unless the owner wants them open.

## Channel identity
Studio and youtube.com often fall back to the owner's personal channel ("Abdullah Osama"). Before any comment: avatar menu →
Switch account → **The Last Hours**. On a watch page you are the channel when it shows "Analytics / Edit video", not "Subscribe".

## Scheduling
- The time field is the browser's **Local Time** and its offset follows the PC clock: it read GMT+03:00 while Egypt was on summer
  time and **GMT+02:00 since 29 Oct 2026** → now type the Cairo time itself (22:00 → 22:00, 19:00 → 19:00). ALWAYS zoom on the
  time-zone chip before scheduling (Egypt summer time returns late April → then the field matches Cairo again, still type Cairo time).
  The "Video scheduled" confirmation prints the time in that same local zone: it must read the Cairo time you meant.
- Date: click the date button → `find` "date text input" → ctrl+a → type "D Mon YYYY" → Enter. Time: click → ctrl+a → type → Enter.
- Visibility panel → Done → page Save. Verify: `document.querySelector('ytcp-button#save').hasAttribute('disabled')` is true.
- Moving a scheduled video to Private = "Save or publish" → Private → Done → Save (never delete).
- **Re-upload swap (30 Oct, 9 files):** read the old copy first (A/B titles, description, tags, playlist; A/B thumbnails matched to the
  local *_upload.jpg by a 32-value grey fingerprint of `/vi/<id>/mqdefault_custom_N.jpg`), then in the new draft's upload dialog
  (`/videos/upload?d=ud&udvid=<id>`): details by JS, A/B "Title and thumbnail" (file inputs via `find`), Video elements → End screen
  "Import from video" (old copy), Visibility → Schedule. Then the old copy: "Edit title" (deletes its A/B test, fine) → "OLD COPY
  (delete) <title>" → Private → Save. End-screen video elements that pointed to an old copy → repoint to the new id (picker search box
  "Search your videos" for anything beyond the first 50). Captions: Languages → Edit subtitles → ⋮ → Upload file → Without timing →
  file input via `find` → Publish (wait ~13 s for the editor before the ⋮ menu).
- Studio's CSP can block `eval` of stored snippets mid-session: send JS inline.

## Element refs (the big trap)
Refs from `find` are page-specific: on a Short that already has a related video, the same ref number can be the **subtitle editor**
or the **remove-related-video X**. Always `find` fresh on each page; after any surprise, check that Save is still disabled and use
"Undo changes" / "Discard changes".

## Upload dialog
- Never press Escape (it closes the dialog into a draft; reopen via Edit draft).
- `file_upload` to the hidden file input (`find` "hidden file input"); the tool's limit is 10 MB per call → long videos are dragged
  in by the owner; Shorts get 2-pass x264 copies under 10 MB.
- Typing `#` in the description opens a hashtag popup: click the "Details" heading to close it.
- Playlist checkboxes: tick by coordinate after opening the list (order changes between dialogs); verify via
  `ytcp-video-metadata-playlists` innerText.
- Not made for kids radio, Show more → tags (comma separated), Video language (plain "English"), Category (Education default).
- Next ×3 via `ytcp-uploads-dialog #next-button`; Visibility → Schedule → date/time → `#done-button`. "We're still checking your
  content" → Got it. Grab the new ID from the dialog's youtube.com/shorts link.

## A/B tests (Test & compare)
- Title-only, thumbnail-only, or title + thumbnail (max 3 variants). Any change to an existing test = "Run a new test? current test
  will be deleted" → rebuild it (re-upload thumbnails from `export/thumbnails/*_upload.jpg` with the pairs in UPLOAD_COPY_PASTE).
  A test on a scheduled video shows "Ineligible: your video is not public" until it goes live (normal).
- Set test → page Save.

## Captions, end screen, related video
- Captions: Languages → add → Upload file → "Without timing" → `file_upload` straight to the hidden input.
- End screen: "Import from video", then the pencil on a video element to change its target.
- Related video (Shorts): edit page → Related video → pick from "Choose specific video" (only public videos). On 29 Oct 2026 the
  picker opened empty on every Short (a Studio glitch); retry later or set it from the owner's Studio/phone.

## Comments
- Post from the watch page as the channel → ⋮ → Pin → confirm → heart. Studio's comment list hides the "Pinned" label after a
  reload: the watch page is authoritative. Remove the "Unresponded" filter to see your own comments.

## Analytics
- Channel: `/analytics/tab-overview|tab-content|tab-build_audience/period-lifetime`. Video: `/video/<id>/analytics/tab-overview|tab-reach_viewers/period-since_publish`.
- Read with `document.querySelector('main').innerText`. The Advanced-mode explore URL with custom metrics can error ("Oops").
- Exact retention curves: Engagement tab → read the pink retention `<path d>` and axis labels with JS.

## Lessons from The Bill, Explained launch (15 Nov 2026)
- **Rebrand an old channel:** Customisation → Profile (banner/picture/watermark through the hidden file inputs; name; handle; description) → Publish. The page width can shift after the crop dialogs, so click Publish by `find` ref, not by coordinate. Then check the public page `youtube.com/@handle`.
- **Bulk private:** Content → Videos (then Shorts) → Select all → Edit → Visibility → Private → Update videos → tick "I understand" → Update. Reversible.
- **Big-file upload worked:** `split -b 9500000` → one `file_upload` per part (a browser_batch counts as ONE call, so the 10 MB limit applies to the whole batch) into a page-made `<input id=claude_parts>` that collects the files → join the parts as a Blob → DataTransfer onto `input[name=Filedata]` → change event. Check that the byte size matches.
- **Captions during processing:** "Without timing" uploads fail ("caption track failed to update") while YouTube is still generating auto-subtitles. Upload a **timed SRT** instead (`tools/the-bill-explained/make_srt.py` writes it from the render's word-timed caption chunks): Edit subtitles → Options → Upload file → With timing → Publish.
- **AI-use question (new wording):** "Was AI used to ... make a real person say/do, alter real footage, realistic scene, music". Our own cloned voice + charts + real photos = **No**.
- **A/B test:** edit page → A/B testing → Thumbnail only → the dialog's file inputs (label them by JS, then `find`) → Set test → page Save.
