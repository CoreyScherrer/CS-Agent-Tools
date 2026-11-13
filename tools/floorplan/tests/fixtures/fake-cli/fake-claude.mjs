// Stands in for `claude` in tests: answers --version, and for `-p` logs its arguments and prompt to
// $FAKE_LOG, then prints the stream-json events a real run would.
import fs from 'node:fs';

const args = process.argv.slice(2);
if (args[0] === '--version') { console.log('2.0.0 (Claude Code, test)'); process.exit(0); }
// $FAKE_RESTRICTED: a newer Claude Code, whose help lists restricted mode
if (args[0] === '--help') { console.log(process.env.FAKE_RESTRICTED ? '  --restricted  Restricted mode\n  --strict-mcp-config  Only use MCP servers from --mcp-config' : '  -p, --print'); process.exit(0); }
let input = '';
process.stdin.on('data', (d) => { input += d; });
process.stdin.on('end', () => {
  fs.appendFileSync(process.env.FAKE_LOG, JSON.stringify({ args, input }) + '\n');
  const out = (ev) => console.log(JSON.stringify(ev));
  out({ type: 'system', subtype: 'init', session_id: 'test-session' });
  // a change to a blueprint: answer with the next reply in $FAKE_CHANGES (a JSON array), one per run
  const schema = args[args.indexOf('--json-schema') + 1] || '';
  if (process.env.FAKE_CHANGES && schema.includes('"architecture"')) {
    const replies = JSON.parse(fs.readFileSync(process.env.FAKE_CHANGES, 'utf8'));
    const counter = process.env.FAKE_CHANGES + '.n';
    const n = fs.existsSync(counter) ? +fs.readFileSync(counter, 'utf8') : 0;
    fs.writeFileSync(counter, String(n + 1));
    out({ type: 'assistant', message: { content: [{ type: 'tool_use', name: 'Read', input: { file_path: 'floorplan/plan.json' } }] } });
    out({ type: 'result', subtype: 'success', is_error: false, session_id: 'test-session', structured_output: replies[Math.min(n, replies.length - 1)] });
    return;
  }
  out({ type: 'assistant', message: { content: [{ type: 'tool_use', name: 'Bash', input: { command: 'node floorplan/query.mjs overview' } }] } });
  out({ type: 'assistant', message: { content: [{ type: 'tool_use', name: 'Read', input: { file_path: 'shop-api/routes/orders.js' } }] } });
  // $FAKE_SPLIT: the answer has a dash, and the two writes cut that character in half, as a pipe can
  if (process.env.FAKE_SPLIT) {
    const line = Buffer.from(JSON.stringify({ type: 'result', subtype: 'success', is_error: false, session_id: 'test-session', structured_output: { title: 'Refunds', answer: 'Refunds \u2014 \u201cmoney back\u201d.', items: [] } }) + '\n');
    const cut = line.indexOf(Buffer.from('\u2014')) + 1;
    process.stdout.write(line.subarray(0, cut));
    setTimeout(() => process.stdout.write(line.subarray(cut)), 200);
    return;
  }
  out({ type: 'result', subtype: 'success', is_error: false, session_id: 'test-session', structured_output: {
    title: 'Refunds', answer: 'Refunds go through [[f:shop-api/routes/orders.js]].',
    items: [{ id: 'f:shop-api/routes/orders.js', note: 'Holds the refund endpoint.' }],
  } });
});
