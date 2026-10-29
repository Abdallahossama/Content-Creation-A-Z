"""Step 4: public /shorts tab of each candidate true-mystery channel (flat, newest 40) -> collected.json for swipe.py."""
import json, subprocess, sys, concurrent.futures as cf
CH = {  # channel_id: name (from search + hashtag scans)
 "UCIbP7As-f9DsLdFMJRwrZLw": "Sofu Causerie", "UCAx6ZKtu5mSGe--JMT14Ssg": "Obscara", "UC28N7UBz-niY8cpoRR2OrsQ": "ONCE UPON A MIC",
 "UC-FuZ2J_RdzibbuaTj6KJLA": "Hidden Giant", "UCASSFGtOHD6HwHg3s1yl-UQ": "Past Vault", "UCC_UFbcBpX7ZNUZKBBVz66w": "Deepigma",
 "UCZVohmoW-NRAwK02xJYA__A": "artloris", "UCTr2GSuQBsh5f4i1YTGWreA": "Buried Fortune", "UCnySI-ej6xP2XkglNAXEC6w": "ForbiddenEchoes",
 "UCXylKvpqTrDlcdbiS46G8lg": "The Dark Curiosities", "UCWQq9DmWkF13ay-57b2Kapg": "PMC Untold", "UCFysV0sC0xOXnyNSfSckp8g": "The Unseen Files",
 "UCPXkSBw0fHPKH5Bm5-5b_-g": "Unknown Files", "UCpXzfMJdaTeWm6Eh8Ci7iOA": "After Dark Archives", "UC3CXTsFslKBc29Qxolr-91w": "Lost Secrets",
 "UCnkr463yPI2bavQYD_OObtg": "The Mystery Dossier", "UCk9EgGBi0CftLZZ_D4qWBhQ": "Untold Files Studio", "UCZ957dNk0uUIwUZAbqvE0OQ": "Mystifystories777",
 "UC-UB8dtzoZ_LLqtZVmAZR0Q": "The Story Behind The Mystery", "UCaeyojbupVChiRg8q9LhFXg": "Unsolved Casebook", "UCU3EzSGj6-f5JYFJk88M4Eg": "Dark Vault Files",
 "UClZV1cQ-6aednKPOSVkIhqA": "Lost n Lazy", "UCojWKwMpp8Q5d1Yh_uY1N2A": "Only The Historical Facts", "UCJsCVPhboTC86ykjm7SH_Xg": "Mind Mystery Studio",
 "UCxBqddyp-44_wy9UPoq8ETg": "Unsealed History", "UCzuAym2qYpvndqCN3gXsH2w": "Global Mystery Files", "UCOYmvtlE6h9xRbL2t8dt2-g": "Themysteryvault",
 "UCSutL5uzkPvwTFA0-f7pn1Q": "History Mystery Shorts", "UCciHpi0okckITLlTs8tolKg": "The Unanswered Files", "UChfcQSZoT9_uH9qnzBnoVgw": "Echoes of Mystery",
 "UCXByH2SfIufzBXR0uRdpKUA": "MysteriesUnveiledAI", "UCDximB4kRw3d6SPcZdfHUuw": "Phantom Findings", "UCr5FMhgjWHOss-lzTAET8bg": "Black Ledger",
 "UCQNIJBgSm5lg0mGTGn19EIQ": "One Minute History", "UCkjAOMMyRzXD5kJq_-15HFg": "Chronicle Nexus", "UCA7ROHyuJ4GtGsWBXJSkiKQ": "MYSTERIUM",
 "UC_Zgf4DKW7cMCb5wP4qR0Pw": "The Fact Vault", "UCQwmyy6M9v3KcF9YmPzkVXQ": "History in Short", "UCcvM-ErW8o4k4bAUlu2gisA": "ODDLY",
 "UCOyjLDJyNZ_YbEDaKA0MMeA": "Chronicles of Curiosity", "UClqO0JHTy0x5e_LnDVtCCwQ": "Dark Fact", "UCi_dummy": "x",
}
def get(cid):
    p = subprocess.run([sys.executable, "-m", "yt_dlp", "--flat-playlist", "-J", "--playlist-end", "40",
                        f"https://www.youtube.com/channel/{cid}/shorts"], capture_output=True, text=True, encoding="utf-8")
    if p.returncode: return cid, None
    return cid, json.loads(p.stdout)
rows, info = [], {}
with cf.ThreadPoolExecutor(6) as ex:
    for cid, j in ex.map(get, [c for c in CH if c != "UCi_dummy"]):
        if not j: print("FAIL", CH[cid]); continue
        name = j.get("channel") or CH[cid]
        es = [e for e in j.get("entries", []) if e.get("view_count") is not None]
        info[name] = {"cid": cid, "subs": j.get("channel_follower_count"), "n": len(es)}
        for k, e in enumerate(es):
            rows.append({"channel": name, "title": e.get("title"), "views": e["view_count"], "url": f"https://www.youtube.com/shorts/{e['id']}",
                         "id": e["id"], "duration": e.get("duration") or 45, "rank": k})
json.dump(rows, open("collected.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(info, open("channels.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for n, v in sorted(info.items(), key=lambda kv: -(kv[1]["subs"] or 0)): print(v["subs"], v["n"], n)
