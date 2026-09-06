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

data.updated_at = bangkokIsoNow();
data.mode = 'CONTROLLED TEST • REEL + LINKED STILL • GLOBAL MARKET';
data.schedule_baseline = {
  timezone: 'Asia/Bangkok',
  reel: '08:30',
  linked_still: '20:30',
  status: 'TESTABLE',
  note: 'Current controlled-test baseline; not a permanent publishing schedule.'
};

for (const row of data.calendar || []) {
  row.time = '08:30 / 20:30';
  const id = String(row.title || '').match(/CS-\d{3}/)?.[0];
  if (id === 'CS-002' || id === 'CS-003') row.publish_status = 'PUBLISHED';
  if (id === 'CS-004') row.publish_status = 'READY';
}

for (const ep of data.episodes || []) {
  ep.reel ||= {};
  ep.still ||= {};

  if (ep.id === 'CS-002' || ep.id === 'CS-003') {
    ep.reel.status = 'published';
    ep.still.status = 'published';
  }
  if (ep.id === 'CS-004') {
    // Preserve truth: production-ready, publication not confirmed.
    if (ep.reel.status === 'published') ep.reel.status = 'waiting';
    if (ep.still.status === 'published') ep.still.status = 'ready';
  }

  // post_time is treated as planned time only for non-published content.
  if (ep.reel.status !== 'published' && 'post_time' in ep.reel) ep.reel.post_time = '08:30';
  if (ep.still.status !== 'published' && 'post_time' in ep.still) ep.still.post_time = '20:30';

  ep.schedule ||= {};
  ep.schedule.timezone = 'Asia/Bangkok';
  ep.schedule.reel = '08:30';
  ep.schedule.linked_still = '20:30';
  ep.schedule.baseline_status = 'TESTABLE';
}

fs.writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
console.log(`Normalized ${path}: ${data.episodes?.length || 0} episodes, ${data.calendar?.length || 0} calendar rows.`);
