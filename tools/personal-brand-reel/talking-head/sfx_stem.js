// SFX stem for CapCut from manifest2.json (same levels as the MP4 mix, incl. the +2 dB master). usage: node sfx_stem.js out.wav
const { execFileSync } = require('child_process'); const M = require('./manifest2.json');
const args = ['-y', '-v', 'error', '-f', 'lavfi', '-t', String(M.T), '-i', 'anullsrc=r=48000:cl=stereo']; const f = ['[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[z]']; const L = ['[z]'];
M.fx.forEach(([file, at, g], i) => { args.push('-i', file); f.push(`[${i + 1}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,volume=${g}dB,adelay=${Math.max(0, Math.round(at * 1000))}:all=1[f${i}]`); L.push(`[f${i}]`); });
f.push(`${L.join('')}amix=inputs=${L.length}:normalize=0:duration=first,volume=2dB[a]`);
args.push('-filter_complex', f.join(';'), '-map', '[a]', '-c:a', 'pcm_s24le', process.argv[2]); execFileSync('ffmpeg', args); console.log('stem', process.argv[2], M.fx.length);
