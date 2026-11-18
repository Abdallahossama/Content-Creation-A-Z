// v2 composite: base2.mov (tight cuts) + voice_pro.wav + B-roll + brand cards/pills/step bar/paper cutaway + captions + SFX + energetic bed (flat, no ducking)
const { execFileSync } = require('child_process'); const fs = require('fs');
const E = require('./edl2_segs.json'); const CAP = require('./caps2.json');
const OUT = process.argv[2] || 'D:/personal brand/02_videos/1st_video_A-to-Z_v2.mp4';
const BR = 'D:/my/BEST_BROLL/', PNG = 'cards/png/', SFX = 'D:/why habibi/_style_kit/sfx/';
const MUSIC = 'D:/why habibi/_music_library/Eternity.mp3', CLICK = 'D:/codebyabdullah_assets/workspace/edit_paper/click.wav';
// timeline
let t = 0; E.forEach(c => { c.t = t; let u = t; c.map = c.segs.map(([p, n]) => { const m = { p, d: n / 30, at: u }; u += n / 30; return m; }); c.d = u - t; t = u; });
const T = +t.toFixed(3);
const tl = (c, src) => { for (const m of c.map) { if (src < m.p) return m.at; if (src < m.p + m.d) return m.at + (src - m.p); } return c.t + c.d; };
fs.writeFileSync('timeline2.json', JSON.stringify(E.map(c => ({ id: c.id, t: +c.t.toFixed(3), d: +c.d.toFixed(3), map: c.map })), null, 1));

const args = ['-y', '-v', 'error', '-stats', '-i', 'base2.mov', '-i', 'voice_pro.wav'];
const fc = ['[0:v]format=yuv420p[v0]']; let k = 2, prev = 'v0', j = 0; const fx = [];
const MAN = { overlays: [], brolls: [], caps: [], fx: null, T: 0 }; const LF = {};
const ov = (label, x, y, s, e, o = {}) => {
  MAN.overlays.push({ file: LF[label], x, y, s, e, scale: o.scale || null });
  const F = o.f ?? 0.12; let f = 'format=rgba';
  if (o.scale) f += `,scale=${o.scale}`;
  if (o.fin !== false) f += `,fade=t=in:st=${s.toFixed(3)}:d=${F}:alpha=1`;
  if (o.fout !== false) f += `,fade=t=out:st=${(e - F).toFixed(3)}:d=${F}:alpha=1`;
  fc.push(`[${label}]${f}[s${j}]`);
  const yy = o.slide ? `'${y}+${o.slide}*pow(max(0\\,1-(t-${s.toFixed(3)})/0.22)\\,2)'` : y;
  fc.push(`[${prev}][s${j}]overlay=x=${x}:y=${yy}:enable='between(t,${s.toFixed(3)},${e.toFixed(3)})'[o${j}]`);
  prev = `o${j}`; j++;
};
const img = (file, dur = T) => { args.push('-loop', '1', '-framerate', '30', '-t', dur.toFixed(2), '-i', file); LF[`${k}:v`] = file; return `${k++}:v`; };

// 1) B-roll
for (const c of E) if (c.broll) {
  const [name, ss] = c.broll; const a = c.t + (c.brollAt || 0), b = c.t + c.d;
  args.push('-ss', String(ss), '-t', (b - a + 0.2).toFixed(2), '-i', BR + name + '.mp4'); MAN.brolls.push({ file: BR + name + '.mp4', ss, a, b });
  // slow push-in on b-roll so it never feels static
  fc.push(`[${k}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,scale=2160:3840:flags=lanczos,perspective=x0='0.5*W*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':y0='0.5*H*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':x1='W-0.5*W*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':y1='0.5*H*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':x2='0.5*W*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':y2='H-0.5*H*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':x3='W-0.5*W*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':y3='H-0.5*H*(1-1/(1+0.025*in/${Math.round((b - a) * 30)}))':interpolation=cubic:eval=frame,scale=1080:1920:flags=lanczos,format=yuv420p,setpts=PTS-STARTPTS+${a.toFixed(3)}/TB[br${k}]`);
  fc.push(`[${prev}][br${k}]overlay=0:0:eof_action=pass:enable='between(t,${a.toFixed(3)},${b.toFixed(3)})'[o${j}]`);
  prev = `o${j}`; j++; k++;
  fx.push([SFX + 'whoosh_fast.wav', a - 0.12, -21]);
}
// 2) paper cutaway (full-screen brand "image")
for (const c of E) if (c.paper) { const a = c.t, b = c.t + 0.62; ov(img(`${PNG}paper_far2.png`), 0, 0, a, b, { fin: false, f: 0.08 }); fx.push([SFX + 'paper_slide.wav', a - 0.05, -18]); fx.push([SFX + 'impact_soft.wav', a, -20]); }
// 3) step progress bar (top) — shows from the first step clip to the end of step 4
const stepClips = E.filter(c => c.step); let lastStep = 0;
for (const c of stepClips) {
  const a = c.t, b = c.t + c.d;
  ov(img(`${PNG}step${c.step}.png`), 40, 70, a, b, { fin: c.step !== lastStep, fout: false, slide: c.step !== lastStep ? -40 : 0, f: 0.1 });
  if (c.step !== lastStep) fx.push([CLICK, a + 0.02, -18]);
  lastStep = c.step;
}
// 4) cards (typed 4 states) during the face part of the clip
for (const c of E) if (c.card) {
  const a = c.t + (c.paper ? 0.66 : 0.12), b = c.t + (c.brollAt || c.d) - 0.04, n = 4;
  const step = Math.min(0.5, (b - a - 0.35) / n);
  for (let i = 0; i < n; i++) {
    const s = a + i * step, e = i < n - 1 ? a + (i + 1) * step : b;
    ov(img(`${PNG}${c.card}${i + 1}.png`), 215, 205, s, e, { scale: '650:-1', fin: i === 0, fout: i === n - 1, slide: i === 0 ? 26 : 0 });
    fx.push([CLICK, s + 0.02, i ? -24 : -21]);
  }
  fx.push([SFX + 'swoosh_in.wav', a - 0.1, -20]);
}
// 5) pop-up pills (brand sticker)
const pills = { hook: ['p_hook', 0.25], ydee3: ['p_ydee3', 0.9], awel: ['p_awel', 1.6], ywafe2: ['p_ywafe2', 0.5], tasleem: ['p_tasleem', 1.2], '3aref': ['p_3aref', 1.0] };
for (const c of E) if (pills[c.id]) {
  const [n, at] = pills[c.id]; const a = c.t + at, b = c.t + c.d - 0.05;
  ov(img(`${PNG}${n}.png`), 40, c.id === 'hook' ? 250 : 215, a, b, { slide: 30, f: 0.1 });
  fx.push([SFX + 'sticker_slap.wav', a, -19]); fx.push([SFX + 'pop.wav', a + 0.02, -22]);
}
// 6) CTA card
const CTA = process.env.CTA; // 'a' = incoming-call card, 'b' = approved card + ringing phone badge
for (const c of E) if (c.cta) {
  fx.push([SFX + 'riser_short.wav', c.t - 0.9, -27]);
  if (!CTA) { ov(img(`${PNG}cta.png`), 160, 200, c.t + 0.2, c.t + c.d, { fout: false, slide: 30 }); fx.push([SFX + 'pop.wav', c.t + 0.2, -18]); fx.push([SFX + 'bell.wav', c.t + 0.25, -24]); continue; }
  const dir = `E:/cta_frames/${CTA}`; args.push('-framerate', '30', '-i', dir + '/f%04d.png'); MAN.overlays.push({ file: dir, seq: true, s: c.t, e: c.t + c.d });
  fc.push(`[${k}:v]format=rgba,setpts=PTS-STARTPTS+${c.t.toFixed(3)}/TB[cta]`);
  fc.push(`[${prev}][cta]overlay=0:0:eof_action=repeat:enable='gte(t,${c.t.toFixed(3)})'[o${j}]`); prev = `o${j}`; j++; k++;
  const T0 = c.t, TAP = c.t + 1.54, SUB = c.t + 3.14, LINK = c.t + 5.43;
  if (CTA === 'a') { fx.push([SFX + 'swoosh_in.wav', T0 + 0.05, -22]); fx.push([SFX + 'phone_ring.wav', T0 + 0.15, -22]); fx.push([CLICK, TAP, -16]); fx.push([SFX + 'pop.wav', TAP + 0.02, -22]); fx.push([CLICK, SUB, -24]); }
  else { fx.push([SFX + 'pop.wav', T0 + 0.2, -18]); fx.push([SFX + 'phone_ring.wav', T0 + 0.45, -22]); fx.push([CLICK, TAP, -17]); fx.push([SFX + 'sticker_slap.wav', SUB, -19]); fx.push([SFX + 'pop.wav', SUB + 0.02, -22]); }
  fx.push([SFX + 'pop.wav', LINK, -20]); fx.push([SFX + 'bell.wav', LINK + 0.05, -24]);
}
// 7) watermark
ov(img(`${PNG}wm.png`), 330, 1830, 0.3, T, { fout: false, f: 0.4 });
// hook hit
fx.push([SFX + 'impact_soft.wav', 0, -18]);

// 8) captions
const ts = x => `0:${String(Math.floor(x / 60)).padStart(2, '0')}:${(x % 60).toFixed(2).padStart(5, '0')}`;
const ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', 'WrapStyle: 2', '', '[V4+ Styles]',
  'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
  'Style: Cap,Alexandria ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H10121212,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,2,90,90,400,1',
  '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'];
for (const c of E) { const L = CAP[c.id]; L.forEach(([txt, src], i) => {
  const s = Math.max(c.t, tl(c, src)), e = i < L.length - 1 ? tl(c, L[i + 1][1]) : c.t + c.d;
  if (c.paper && i === 0) return; // the paper card says it
  MAN.caps.push({ txt, s, e });
  ass.push(`Dialogue: 0,${ts(s)},${ts(e - 0.01)},Cap,,0,0,0,,{\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}\u200F${txt}`);
}); }
fs.writeFileSync('captions2.ass', ass.join('\n') + '\n', 'utf8');
fc.push(`[${prev}]ass=captions2.ass:fontsdir=D\\\\:/codebyabdullah_assets/workspace/edit/fonts:shaping=complex,format=yuv420p[vout]`);

// 9) audio: clean voice + sfx + flat music bed (no ducking / pumping)
const mix = ['[1:a]aresample=48000,aformat=channel_layouts=stereo[voice]']; const lab = ['[voice]'];
fx.forEach(([f, at, g], i) => { args.push('-i', f); mix.push(`[${k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=${g}dB,adelay=${Math.max(0, Math.round(at * 1000))}:all=1[fx${i}]`); lab.push(`[fx${i}]`); k++; });
args.push('-i', MUSIC);
mix.push(`[${k}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:${T + 1},asetpts=PTS-STARTPTS,highpass=f=60,equalizer=f=2500:t=q:w=1.5:g=-4,volume=-22.5dB,afade=t=in:d=0.25,afade=t=out:st=${(T - 1.6).toFixed(2)}:d=1.6[bed]`); lab.push('[bed]');
mix.push(`${lab.join('')}amix=inputs=${lab.length}:normalize=0:duration=first,volume=2dB,alimiter=limit=0.89:level=false,aresample=48000[aout]`);
MAN.fx = fx; MAN.T = T; MAN.musicChain = mix[mix.length - 2]; fs.writeFileSync('manifest2.json', JSON.stringify(MAN, null, 1));
if (process.env.DRY) { console.log('manifest only'); process.exit(0); }
fs.writeFileSync('filter_v2.txt', fc.concat(mix).join(';\n'), 'utf8');
args.push('-filter_complex_script', 'filter_v2.txt', '-map', '[vout]', '-map', '[aout]', '-t', String(T),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '192k', OUT);
fs.mkdirSync(require('path').dirname(OUT), { recursive: true });
execFileSync('ffmpeg', args, { stdio: 'inherit' });
console.log('done', OUT, T);
