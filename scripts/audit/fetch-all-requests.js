#!/usr/bin/env node
/**
 * Загрузка всех заявок U-ON по ID (1..MAX_ID)
 * Использует параллельные батчи по 8 запросов (с учётом лимита 10 req/sec)
 */
require('dotenv').config({ path: require('path').join(__dirname, '../../.env') });
const https = require('https');
const fs = require('fs');
const path = require('path');

const KEY = process.env.UON_API_KEY;
const MAX_ID = 1300;
const BATCH = 8;
const DELAY = 900; // ms between batches → ~8 req/900ms < 10 req/sec

function fetchRequest(id) {
  return new Promise((resolve) => {
    const url = `https://api.u-on.ru/${KEY}/request/${id}.json`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          const r = j?.request?.[0];
          if (r && r.id) resolve(r);
          else resolve(null);
        } catch { resolve(null); }
      });
    }).on('error', () => resolve(null));
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log(`Загружаю заявки U-ON (ID 1..${MAX_ID}), батчи по ${BATCH}...`);
  const results = [];
  let nullCount = 0;

  for (let start = 1; start <= MAX_ID; start += BATCH) {
    const ids = Array.from({ length: BATCH }, (_, i) => start + i).filter(i => i <= MAX_ID);
    const batch = await Promise.all(ids.map(fetchRequest));
    const valid = batch.filter(Boolean);
    results.push(...valid);
    const nulls = batch.filter(x => !x).length;
    nullCount += nulls;

    process.stdout.write(`\r  ID ${start}-${start + BATCH - 1}: +${valid.length} заявок, итого ${results.length}, пропущено ${nullCount}`);
    if (start + BATCH <= MAX_ID) await sleep(DELAY);
  }

  console.log(`\n\nВсего загружено: ${results.length} заявок`);

  const outPath = path.join(__dirname, '../../docs/audit/uon-raw-2026.json');
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
  console.log(`Сохранено: ${outPath}`);
}

main().catch(e => { console.error(e.message); process.exit(1); });
