const {execFileSync}=require('child_process');const fs=require('fs');
const C=require('./cands.json');const SRC='D:/my/1st video/20261118_131509.mp4';
const FONT="arialbd.ttf";
for(const [line,takes] of Object.entries(C)){
  const tiles=[];
  takes.forEach(([a,b],i)=>{
    const d=b-a;[0.25,0.5,0.8].forEach((f,j)=>{
      const t=(a+d*f).toFixed(2), out=`cand/${line.split(' ')[0]}_${i}_${j}.jpg`;
      execFileSync('ffmpeg',['-y','-v','error','-ss',t,'-i',SRC,'-frames:v','1','-vf',`hflip,scale=180:-2,crop=180:200:0:40,drawtext=fontfile=${FONT}:text='T${i} ${a}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black`,out]);
      tiles.push(out);});
  });
  const n=takes.length, rows=n, inputs=tiles.flatMap(f=>['-i',f]);
  const lay=tiles.map((_,k)=>`${(k%3)*180}_${Math.floor(k/3)*200}`).join('|');
  execFileSync('ffmpeg',['-y','-v','error',...inputs,'-filter_complex',`xstack=inputs=${tiles.length}:layout=${lay}`,'-frames:v','1',`cand/sheet_${line.split(' ')[0]}.jpg`]);
}
console.log('ok');
