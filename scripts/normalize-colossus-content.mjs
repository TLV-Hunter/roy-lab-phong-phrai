import fs from 'node:fs';

const contentPath = 'colossus/content.json';
const reelMediaPath = 'colossus/colossus-reel-media.json';
const indexPath = 'colossus/index.html';

const data = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const reelMedia = fs.existsSync(reelMediaPath)
  ? JSON.parse(fs.readFileSync(reelMediaPath, 'utf8'))
  : {entries:[]};

function bangkokIsoNow(){
  const now = new Date();
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone:'Asia/Bangkok', year:'numeric', month:'2-digit', day:'2-digit',
    hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:false
  }).formatToParts(now).reduce((a,p)=>(a[p.type]=p.value,a),{});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+07:00`;
}

function publishState(ep){
  const r = String(ep?.reel?.status || 'waiting').toLowerCase();
  const s = String(ep?.still?.status || 'ready').toLowerCase();
  if (r === 'published' && s === 'published') return 'PUBLISHED';
  if (r === 'published') return `REEL PUBLISHED • STILL ${s.toUpperCase()}`;
  if (s === 'published') return `STILL PUBLISHED • REEL ${r.toUpperCase()}`;
  if (r === 'scheduled' || s === 'scheduled') return 'SCHEDULED';
  if (r === 'ready' || s === 'ready') return 'READY';
  return 'WAITING';
}

const mediaById = new Map((reelMedia.entries || []).map(x => [x.id, x]));
const registryReady = new Set(
  (reelMedia.entries || [])
    .filter(x => /ready|published/i.test(String(x.status || '')))
    .map(x => x.id)
);

// Explicit latest user correction: CS-022 Final exists. Exact media URL remains pending safe re-mapping.
registryReady.add('CS-022');

// Existing earlier Finals that predate the current media overlay registry.
const legacyReady = new Set(['CS-005','CS-007','CS-008']);
const confirmedBoth = new Set(['CS-002','CS-003','CS-004','CS-006']);
const confirmedStill = new Set(['CS-005','CS-007','CS-008']);
const confirmedReel = new Set(['CS-009']);

data.updated_at = bangkokIsoNow();
data.mode = 'CONTROLLED TEST • REEL + LINKED STILL • GLOBAL MARKET';
data.schedule_baseline = {
  timezone: 'Asia/Bangkok',
  reel: '08:30',
  linked_still: '20:30',
  status: 'TESTABLE',
  note: 'Current controlled-test baseline; not a permanent publishing schedule.'
};

for (const ep of data.episodes || []) {
  ep.reel ||= {};
  ep.still ||= {};

  // Never regress explicit publication truth.
  if (confirmedBoth.has(ep.id)) {
    ep.reel.status = 'published';
    ep.still.status = 'published';
  }
  if (confirmedStill.has(ep.id)) ep.still.status = 'published';
  if (confirmedReel.has(ep.id)) ep.reel.status = 'published';

  if (ep.reel.status !== 'published' && (registryReady.has(ep.id) || legacyReady.has(ep.id))) {
    ep.reel.status = 'ready';
  }

  // CS-009 linked still has not been explicitly confirmed published in current source truth.
  if (ep.id === 'CS-009' && ep.still.status !== 'published') ep.still.status = 'ready';

  const media = mediaById.get(ep.id);
  if (media) {
    ep.reel.final_exists = /ready|published/i.test(String(media.status || ''));
    if (media.media_url) ep.reel.final_media_url = media.media_url;
    if (media.qa) ep.reel.final_qa = media.qa;
    if (media.media_link_status) ep.reel.media_link_status = media.media_link_status;
  }
  if (ep.id === 'CS-022') {
    ep.reel.final_exists = true;
    ep.reel.media_link_status = 'PENDING CORRECT MAPPING';
    ep.reel.final_qa = 'FINAL EXISTS — USER CONFIRMED';
  }

  if (ep.reel.status !== 'published' && 'post_time' in ep.reel) ep.reel.post_time = '08:30';
  if (ep.still.status !== 'published' && 'post_time' in ep.still) ep.still.post_time = '20:30';

  ep.schedule ||= {};
  ep.schedule.timezone = 'Asia/Bangkok';
  ep.schedule.reel = '08:30';
  ep.schedule.linked_still = '20:30';
  ep.schedule.baseline_status = 'TESTABLE';
}

const byId = new Map((data.episodes || []).map(ep => [ep.id, ep]));
for (const row of data.calendar || []) {
  row.time = '08:30 / 20:30';
  const id = String(row.title || '').match(/CS-\d{3}/)?.[0];
  if (id && byId.has(id)) row.publish_status = publishState(byId.get(id));
}

const septemberIds = (data.calendar || [])
  .filter(row => String(row.date || '').startsWith('2026-09-'))
  .map(row => String(row.title || '').match(/CS-\d{3}/)?.[0])
  .filter(Boolean);
const missingSeptemberReels = septemberIds.filter(id => {
  const ep = byId.get(id);
  return !['ready','published'].includes(String(ep?.reel?.status || '').toLowerCase());
});

data.production_summary = {
  as_of: bangkokIsoNow(),
  september: {
    still_production: 'COMPLETE',
    still_scope: 'CS-002–CS-028',
    still_master_batch: 'CS-004–CS-029 = 26/26 PASS / ARCHIVED',
    still_publish_caught_up_through: '2026-09-10',
    reel_production: missingSeptemberReels.length ? 'IN PROGRESS' : 'COMPLETE',
    today_reel: 'CS-009 — THE SHADOW BEHIND JUPITER',
    today_reel_status: 'PUBLISHED',
    ready_note: 'CS-022 Final exists per latest user confirmation; correct media URL still requires safe re-mapping.',
    remaining_reels: missingSeptemberReels.join(', ') || 'NONE',
    remaining_reel_count: missingSeptemberReels.length,
    season_finale: 'CS-029 — 2026-10-01'
  },
  note: `Still production is complete. September Reel production has ${missingSeptemberReels.length} unresolved episode(s): ${missingSeptemberReels.join(', ') || 'none'}.`
};

fs.writeFileSync(contentPath, JSON.stringify(data, null, 2) + '\n');

// Keep Content Desk Reel display synced with the current verified media registry.
if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf8');

  const oldLoader = "Promise.all([getJson('./content.json'),getJson('./rls-content.json'),getJson('./rls-starters.json'),getJson('./rls-copy-qa.json'),getJson('./colossus-starters.json').catch(()=>({entries:[]})),getJson('./colossus-reels.json').catch(()=>({entries:[]}))]).then(([c,r,s,q,cs,cr])=>{C=c;R=r;S=s;Q=q;CS=cs;CR=cr;renderAll()})";
  const newLoader = "Promise.all([getJson('./content.json'),getJson('./rls-content.json'),getJson('./rls-starters.json'),getJson('./rls-copy-qa.json'),getJson('./colossus-starters.json').catch(()=>({entries:[]})),getJson('./colossus-reels.json').catch(()=>({entries:[]})),getJson('./colossus-reel-media.json').catch(()=>({entries:[]}))]).then(([c,r,s,q,cs,cr,crm])=>{C=c;R=r;S=s;Q=q;CS=cs;let mm=new Map((crm.entries||[]).map(x=>[x.id,x]));CR={...cr,entries:(cr.entries||[]).map(x=>({...x,...(mm.get(x.id)||{})}))};for(let m of crm.entries||[]){if(!(CR.entries||[]).some(x=>x.id===m.id))CR.entries.push(m)}renderAll()})";
  if (html.includes(oldLoader)) html = html.replace(oldLoader, newLoader);

  html = html.replace(
    /function colReelSlot\(e\)\{[\s\S]*?\}\nfunction rlsCard/,
    `function colReelSlot(e){let r=colReelEntry(e.id),u=r.media_url||'',q=r.copy_qa||'',exists=!!u||/ready|published/i.test(String(r.status||'')),media=u?\`<iframe src="\${esc(driveView(u))}" allow="autoplay"></iframe>\`:exists?\`<div class="waiting"><b>FINAL EXISTS • MEDIA LINK PENDING</b>Final Reel ของตอนนี้มีแล้ว แต่ยังไม่ได้ผูกลิงก์ไฟล์ที่ตรวจสอบถูกต้องเข้ากับเว็บ</div>\`:\`<div class="waiting"><b>FINAL REEL NOT YET UPLOADED</b>เมื่อ Final Reel ผ่าน QA และอัปโหลดแล้ว ระบบจะแสดงในช่องนี้</div>\`;return \`<div class="slot reelslot"><div class="slothead"><b>REEL • FINAL</b><span class="pill \${cls(r.status||'waiting')}">\${esc((r.status||'WAITING').toUpperCase())}\${r.qa?' • '+esc(r.qa):''}</span></div><div class="viewer">\${media}</div><div class="actions">\${u?\`<a href="\${esc(u)}" target="_blank">OPEN FINAL REEL</a><a href="\${esc(driveDl(u))}" target="_blank">DOWNLOAD FINAL</a>\`:exists?\`<span class="pill a">MEDIA LINK PENDING</span><span></span>\`:\`<span></span><span></span>\`}</div>\${copyBlock('REEL CAPTION',r.caption,q,'crcap-'+e.id)}\${copyBlock('REEL FIRST COMMENT',r.pinned_comment,q,'crpin-'+e.id)}</div>\`}\nfunction rlsCard`
  );

  html = html.replace(
    "finalReady=CAM==='rls'?!!r.media_url:!!rr.media_url;return",
    "finalReady=CAM==='rls'?!!r.media_url:(!!rr.media_url||/ready|published/i.test(String(rr.status||''))),finalLink=CAM==='rls'?!!r.media_url:!!rr.media_url;return"
  );
  html = html.replace(
    "<td class=\"${finalReady?'g':'a'}\">${finalReady?'READY':'WAITING'}</td>",
    "<td class=\"${finalReady?'g':'a'}\">${finalReady?(finalLink?'READY':'READY / LINK PENDING'):'WAITING'}</td>"
  );

  const script = html.match(/<script>([\s\S]*)<\/script>/)?.[1];
  if (!script) throw new Error('Content Desk inline script not found');
  new Function(script);
  fs.writeFileSync(indexPath, html);
}

console.log(`Normalized ${contentPath}: September Reel remaining = ${missingSeptemberReels.length} [${missingSeptemberReels.join(', ')}].`);
