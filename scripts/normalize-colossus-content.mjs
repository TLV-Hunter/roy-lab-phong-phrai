import fs from 'node:fs';

const path = 'colossus/content.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));

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

data.updated_at = bangkokIsoNow();
data.mode = 'CONTROLLED TEST • REEL + LINKED STILL • GLOBAL MARKET';

data.schedule_baseline = {
  timezone: 'Asia/Bangkok',
  reel: '08:30',
  linked_still: '20:30',
  status: 'TESTABLE',
  note: 'Current controlled-test baseline; not a permanent publishing schedule.'
};

// Latest confirmed production/publishing truth as of 2026-09-11 morning.
// Preserve anything already marked published; never regress publication truth.
const confirmedBoth = new Set(['CS-002','CS-003','CS-004','CS-006']);
const confirmedStill = new Set(['CS-005','CS-007','CS-008']);
const confirmedReel = new Set(['CS-009']);
const reelReady = new Set(['CS-007','CS-008']);

for (const ep of data.episodes || []) {
  ep.reel ||= {};
  ep.still ||= {};

  if (confirmedBoth.has(ep.id)) {
    ep.reel.status = 'published';
    ep.still.status = 'published';
  }
  if (confirmedStill.has(ep.id)) {
    ep.still.status = 'published';
  }
  if (confirmedReel.has(ep.id)) {
    ep.reel.status = 'published';
  }
  if (reelReady.has(ep.id) && ep.reel.status !== 'published') {
    ep.reel.status = 'ready';
  }

  // CS-005 Reel is not explicitly confirmed in current project evidence.
  if (ep.id === 'CS-005' && ep.reel.status !== 'published') {
    ep.reel.status = 'unverified';
  }

  // CS-009 linked still is not due yet on the morning of Sep 11 under the current baseline.
  if (ep.id === 'CS-009' && ep.still.status !== 'published') {
    ep.still.status = 'ready';
  }

  // Planned times only apply to content that is not already published.
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

data.production_summary = {
  as_of: '2026-09-11T10:02:55+07:00',
  september: {
    still_production: 'COMPLETE',
    still_scope: 'CS-002–CS-028',
    still_master_batch: 'CS-004–CS-029 = 26/26 PASS / ARCHIVED',
    still_publish_caught_up_through: '2026-09-10',
    reel_production: 'IN PROGRESS',
    today_reel: 'CS-009 — THE SHADOW BEHIND JUPITER',
    today_reel_status: 'PUBLISHED',
    remaining_reels: 'CS-010–CS-028',
    remaining_reel_count: 19,
    season_finale: 'CS-029 — 2026-10-01'
  },
  note: 'Still production for the September run is complete. Daily still publishing is caught up through the last due slot. Reel production for the rest of September is not complete.'
};

fs.writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
console.log(`Normalized ${path}: ${data.episodes?.length || 0} episodes, ${data.calendar?.length || 0} calendar rows.`);
