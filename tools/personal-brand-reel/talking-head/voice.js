const {execFileSync}=require('child_process');const E=require('./edl2_segs.json');
const OUT=process.argv[2]||'voice_raw.wav';
const parts=[];const fc=[];let i=0;
for(const c of E)for(const [p,n] of c.segs){const d=n/30;fc.push(`[0:a]atrim=start=${p}:duration=${d.toFixed(5)},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st=${(d-0.015).toFixed(4)}:d=0.015[a${i}]`);parts.push(`[a${i}]`);i++;}
fc.push(`${parts.join('')}concat=n=${i}:v=0:a=1[out]`);
require('fs').writeFileSync('voice_fc.txt',fc.join(';\n'));
execFileSync('ffmpeg',['-y','-v','error','-i','src48.wav','-filter_complex_script','voice_fc.txt','-map','[out]','-ar','48000','-ac','1',OUT]);console.log('ok',OUT);
