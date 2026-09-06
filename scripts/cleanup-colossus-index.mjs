import fs from 'node:fs';

const path = 'colossus/index.html';
let html = fs.readFileSync(path, 'utf8');

// 1) Correct the HTML escaping typo. Keep this idempotent.
html = html.replace("'\"':'&quot',", "'\"':'&quot;',");

// 2) Eliminate hard-coded thumbnail ranges only if the legacy function still exists.
if (html.includes('function hasLocalThumb(id)')) {
  const start = html.indexOf('function hasLocalThumb(id)');
  const end = html.indexOf('function renderChecklist()', start);
  if (start < 0 || end < 0) throw new Error('Thumbnail function anchors not found');
  const replacement = `function thumbFallback(img,id){let w=img.closest('.previewWrap');if(w)w.innerHTML=\`<div class="thumbPending">\${esc(id||'')}<br>LOCAL THUMB<br>NOT CACHED</div>\`}window.thumbFallback=thumbFallback;function thumbHtml(id){let safe=esc(id||'');return \`<div class="previewWrap"><img src="./thumbs/\${safe}.svg?v=3" alt="\${safe} master thumbnail" loading="lazy" onerror="thumbFallback(this,'\${safe}')"></div>\`} `;
  html = html.slice(0, start) + replacement + html.slice(end);
}

// 3) Avoid private Google Drive iframe black/blank preview in DESK.
// Patch only the legacy media function; do nothing if local preview is already active.
if (!html.includes('LOCAL PREVIEW NOT CACHED')) {
  const start = html.indexOf('function media(e)');
  const end = html.indexOf('function pane(e,type)', start);
  if (start < 0 || end < 0) throw new Error('Media function anchors not found');
  const replacement = `function media(e){let p=e.still||{},u=p.media_url||'',id=driveId(u),eid=esc(e.id||'');if(!u)return'<div class="warn">ยังไม่มี Master Image URL</div>';return \`<div class="media"><div class="driveFrame" style="display:flex;align-items:center;justify-content:center"><img src="./thumbs/\${eid}.svg?v=3" alt="\${eid} master preview" loading="lazy" style="width:100%;height:100%;object-fit:contain" onerror="this.style.display='none';this.parentElement.innerHTML='<div class=&quot;thumbPending&quot;>LOCAL PREVIEW NOT CACHED<br>USE OPEN MASTER</div>'"></div><div class="mediaActions"><a href="\${esc(u)}" target="_blank">OPEN MASTER</a><a href="\${driveDownload(u)}" target="_blank">DOWNLOAD 4K</a><button onclick="copyMaster('\${id}','\${esc(u)}')">COPY IMAGE</button><a href="./plan.html#publisher">USE IN PUBLISHER</a></div></div>\`} `;
  html = html.slice(0, start) + replacement + html.slice(end);
}

// 4) Make mixed Reel/Still state explicit instead of letting Reel WAITING hide Still READY.
if (!html.includes('function statusLabel(e)')) {
  const anchor = 'function renderDesk()';
  const at = html.indexOf(anchor);
  if (at < 0) throw new Error('renderDesk anchor not found');
  const fn = `function statusLabel(e){let r=String(e.reel?.status||'—').toUpperCase(),s=String(e.still?.status||'—').toUpperCase();if(r==='PUBLISHED'&&s==='PUBLISHED')return 'PUBLISHED';if(r===s)return r;return \`REEL \${r} • STILL \${s}\`} `;
  html = html.slice(0, at) + fn + html.slice(at);
}
html = html.replace(
  `<span class="pill \${cls(e.reel?.status||e.still?.status)}">\${esc((e.reel?.status||e.still?.status||'—').toUpperCase())}</span>`,
  `<span class="pill \${cls((e.reel?.status==='published'&&e.still?.status==='published')?'published':e.reel?.status||e.still?.status)}">\${esc(statusLabel(e))}</span>`
);

// 5) Parse-check the inline JavaScript before saving.
const script = html.match(/<script>([\s\S]*)<\/script>/)?.[1];
if (!script) throw new Error('Inline script not found');
new Function(script);

fs.writeFileSync(path, html);
console.log('Colossus index cleanup applied and JavaScript parse-check passed.');
