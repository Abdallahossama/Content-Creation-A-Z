const fs=require('fs');
const INK='#121212',PIS='#B9DD74',PAPER='#F3EEE3';
const FONT='file:///D:/codebyabdullah_assets/workspace/edit/fonts/Alexandria-ExtraBold.ttf';
const CSS=`@font-face{font-family:A;src:url('${FONT}')}html,body{margin:0;background:transparent;overflow:hidden}*{box-sizing:border-box}
.pn{position:absolute;inset:0;background-color:${INK};border:2px solid ${PIS};border-radius:14px;overflow:hidden;direction:rtl;
 background-image:linear-gradient(rgba(243,238,227,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(243,238,227,.05) 1px,transparent 1px);background-size:24px 24px}
.hd{height:64px;border-bottom:1px solid rgba(185,221,116,.45);display:flex;align-items:center;gap:14px;padding:0 22px;background:${INK}}
.hd b{font-family:Consolas,monospace;font-weight:400;font-size:20px;color:${INK};background:${PIS};padding:2px 10px;direction:ltr}
.hd span{font-family:A,sans-serif;font-size:30px;color:${PAPER}}
.ls{padding:16px 24px;display:flex;flex-direction:column;gap:12px}
.it{font-family:A,sans-serif;font-size:27px;color:${PAPER};display:flex;align-items:center;gap:14px;line-height:1.35}
.it i{width:12px;height:12px;border:2px solid rgba(243,238,227,.5);flex:none;display:block}
.it.ok i{background:${PIS};border-color:${PIS}}
.it.dim{color:rgba(243,238,227,.55)}
.it.hl span{background:${PIS};color:${INK};padding:0 10px;border-radius:4px}`;
const jobs=[];const W=520,H=300;
const page=(n,w,h,body)=>{fs.writeFileSync(`html/${n}.html`,`<!doctype html><html><head><meta charset="utf-8"><style>${CSS}body{width:${w}px;height:${h}px;position:relative}</style></head><body>${body}</body></html>`);jobs.push(`${n}|${w}|${h}`)};
const card=(p,num,title,items)=>items.forEach((_,k)=>page(`${p}${k+1}`,W,H,`<div class="pn"><div class="hd"><b>${num}</b><span>${title}</span></div><div class="ls">${items.slice(0,k+1).map(([t,c])=>`<div class="it ${c||''}"><i></i><span>${t}</span></div>`).join('')}</div></div>`));
card('bf','00','الوضع الحالي',[['الطلبات على ملف إكسل'],['المتابعة على واتساب'],['«الطلب ده عند مين؟»','dim'],['طلب ضاع النهارده','hl']]);
card('an','01','نفهم الشغل الأول',[['مين بيعمل إيه'],['الطلب بيمشي إزاي'],['الوقت بيضيع فين'],['لسه ولا سطر كود','hl']]);
card('prd','02','مستند واحد واضح',[['الأهداف'],['مين هيستخدم النظام'],['كل المطلوب بالتفصيل'],['العميل وافق قبل التنفيذ','ok']]);
card('bd','03','التنفيذ على مراحل',[['أسبوع ١: الأساس','ok'],['أسبوع ٢: لوحة التحكم','ok'],['أسبوع ٣: التقارير'],['العميل بيجرّب بإيده','hl']]);
card('ho','04','التسليم',[['تدريب الفريق','ok'],['شرح مكتوب','ok'],['دعم بعد التسليم','ok'],['مش هتبقى لوحدك','hl']]);
card('af','05','بعد النظام',[['الطلبات في مكان واحد','ok'],['المتابعة أوتوماتيك','ok'],['كل حاجة واضحة','ok'],['ولا طلب بيضيع','hl']]);
['التحليل','المستند','التنفيذ','التسليم'].forEach((t,i)=>page(`tag${i+1}`,420,80,`<div style="position:absolute;inset:0;display:grid;place-items:center"><span style="font-family:A,sans-serif;font-size:30px;color:${PIS};background:rgba(18,18,18,.9);border:1.5px solid ${PIS};padding:6px 20px 9px;direction:rtl"><span style="font-family:Consolas,monospace;font-size:22px;margin-left:12px">0${i+1}</span>${t}</span></div>`));
fs.writeFileSync('render_list.txt',jobs.join('\n'));console.log(jobs.length);
