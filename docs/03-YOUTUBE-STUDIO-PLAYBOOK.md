# YouTube Studio playbook (browser automation: Claude in Chrome)

Work in **your own new tab**; never navigate or force-navigate a tab the owner uses (uploads may be running: a "Leave site?" dialog
means an upload is in progress). Close your tabs when done unless the owner wants them open.

## Channel identity
Studio and youtube.com often fall back to the owner's personal channel ("Abdullah Osama"). Before any comment: avatar menu →
Switch account → **The Last Hours**. On a watch page you are the channel when it shows "Analytics / Edit video", not "Subscribe".

## Scheduling
- The time field is "Local Time (GMT+0300)", a **fixed +3 offset**; the time-zone dropdown reinterprets, it does not convert.
  Cairo: UTC+3 until the last Thursday of October, UTC+2 after → for 22:00 Cairo in Nov type 23:00; for 19:00 type 20:00.
- Date: click the date button → `find` "date text input" → ctrl+a → type "D Mon YYYY" → Enter. Time: click → ctrl+a → type → Enter.
- Visibility panel → Done → page Save. Verify: `document.querySelector('ytcp-button#save').hasAttribute('disabled')` is true.
- Moving a scheduled video to Private = "Save or publish" → Private → Done → Save (never delete).

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
