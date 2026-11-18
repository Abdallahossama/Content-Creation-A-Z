// v3 face segments: grade -> smooth sub-pixel push-in (perspective, cubic) -> optional per-segment curves (shot match)
const {execFileSync}=require('child_process');const fs=require('fs');
const E=require('./edl2_segs.json');const SRC='D:/my/1st video/20261118_131509.mp4';
const CUR=fs.existsSync('match.json')&&process.argv[2]!=='nomatch'?require('./match.json'):{};
const grade=fs.readFileSync('grade.txt','utf8').replace(/\s*\n\s*/g,'').replace('[v]','[g]');
const list=[];let k=0,alt=0;
E.forEach(c=>c.segs.forEach(([p,n])=>{
  const z0=alt++%2?1.10:1.0, PUSH=0.025;
  const Z=`(${z0}*(1+${PUSH}*in/${n}))`;
  const L=`(0.5*W*(1-1/${Z}))`,T=`(0.35*H*(1-1/${Z}))`,R=`(${L}+W/${Z})`,B=`(${T}+H/${Z})`;
  const per=`perspective=x0='${L}':y0='${T}':x1='${R}':y1='${T}':x2='${L}':y2='${B}':x3='${R}':y3='${B}':interpolation=cubic:eval=frame`;
  const cv=CUR[k]?`,curves=all='${CUR[k]}'`:'';
  const fc=grade+`;[g]setpts=PTS-STARTPTS,scale=2160:3840:flags=lanczos,${per},scale=1080:1920:flags=lanczos${cv},setsar=1,fps=30,format=yuv420p[v]`;
  const out=`seg2/s${String(k).padStart(3,'0')}.mov`;
  execFileSync('ffmpeg',['-y','-v','error','-ss',String(p),'-i',SRC,'-loop','1','-t',(n/30+0.3).toFixed(2),'-i','ellipse.png','-filter_complex',fc,'-map','[v]','-frames:v',String(n),'-an','-c:v','libx264','-preset','fast','-crf','14','-g','15',out]);
  list.push(`file '${out}'`);k++;process.stdout.write('.');
}));
fs.writeFileSync('segs2.txt',list.join('\n'));
execFileSync('ffmpeg',['-y','-v','error','-f','concat','-safe','0','-i','segs2.txt','-c','copy','base2.mov']);
console.log('\nbase2 ok',k);
