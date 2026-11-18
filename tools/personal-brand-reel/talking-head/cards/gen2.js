const fs=require('fs');
const INK='#121212',PIS='#B9DD74',PAPER='#F3EEE3';
const FONT='file:///D:/codebyabdullah_assets/workspace/edit/fonts/Alexandria-ExtraBold.ttf';
const base=`@font-face{font-family:A;src:url('${FONT}')}html,body{margin:0;background:transparent;overflow:hidden}*{box-sizing:border-box}body{position:relative;direction:rtl;font-family:A,sans-serif}`;
const jobs=[];const page=(n,w,h,css,body)=>{fs.writeFileSync(`html/${n}.html`,`<!doctype html><html><head><meta charset="utf-8"><style>${base}body{width:${w}px;height:${h}px}${css}</style></head><body>${body}</body></html>`);jobs.push(`${n}|${w}|${h}`)};
// pills
const pills={p_ydee3:'فلوس بتضيع',p_awel:'ولا سطر كود',p_ywafe2:'موافقة قبل التنفيذ ✓',p_hook:'«عايز سيستم… بس منين؟»',p_tasleem:'✓ النظام شغّال',p_3aref:'كل حاجة قدامك'};
for(const [n,t] of Object.entries(pills))page(n,1000,220,`.w{position:absolute;inset:0;display:grid;place-items:center}.p{display:inline-block;background:${PIS};color:${INK};font-size:62px;line-height:1.25;padding:14px 38px 22px;border:4px solid ${INK};border-radius:18px;box-shadow:10px 10px 0 ${INK};transform:rotate(-2deg)}`,`<div class="w"><div class="p">${t}</div></div>`);
// step bar
const st=['التحليل','المستند','التنفيذ','التسليم'];
for(let a=1;a<=4;a++)page(`step${a}`,1000,110,`.b{position:absolute;inset:10px 20px;display:flex;gap:10px}.s{flex:1;border-radius:12px;display:flex;align-items:center;justify-content:center;gap:10px;font-size:28px;border:2px solid rgba(243,238,227,.35);color:rgba(243,238,227,.6);background:rgba(18,18,18,.78)}.s b{font-family:Consolas,monospace;font-weight:700;font-size:22px}.s.d{border-color:${PIS};color:${PIS}}.s.a{background:${PIS};border-color:${PIS};color:${INK}}`,
 `<div class="b">${st.map((t,i)=>`<div class="s ${i+1<a?'d':i+1===a?'a':''}"><b>0${i+1}</b>${i+1<a?'✓ ':''}${t}</div>`).join('')}</div>`);
// paper cutaway
page('paper_far2',1080,1920,`.pp{position:absolute;inset:0;background:${PAPER};background-image:linear-gradient(rgba(18,18,18,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(18,18,18,.06) 1px,transparent 1px);background-size:54px 54px}
.t{position:absolute;top:640px;left:0;right:0;text-align:center;font-size:190px;color:${INK}}.t span{background:linear-gradient(transparent 58%,${PIS} 58%,${PIS} 92%,transparent 92%);padding:0 20px}
.k{position:absolute;bottom:200px;left:0;right:0;text-align:center;font-family:Consolas,monospace;font-size:34px;color:rgba(18,18,18,.55);direction:ltr}`,`<div class="pp"></div><div class="t"><span>والفرق؟</span></div><div class="k">codebyabdullah</div>`);
// watermark
page('wm',420,70,`.m{position:absolute;inset:0;display:grid;place-items:center;font-family:Consolas,monospace;font-size:30px;color:rgba(243,238,227,.75);direction:ltr;text-shadow:0 2px 6px rgba(0,0,0,.5)}.m i{color:${PIS};font-style:normal}`,`<div class="m"><span><i>●</i> codebyabdullah</span></div>`);
fs.writeFileSync('render_list.txt',jobs.join('\n'));console.log(jobs.length);
