const mineflayer = require('mineflayer');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// ---------- КОНФИГ ----------
const PARTY_TARGET = 'zOkaIchIk17179';           // ник, которому шлём /party
const PARTY_COMMAND = `/party ${PARTY_TARGET}`;

const SERVER_HOST = 'mc.mineblaze.net';        // адрес сервера
const SERVER_PORT = 25565;                     // порт сервера
const BOT_VERSION = '1.16.5';                  // <-- при необходимости поменяй (например '1.12.2', '1.20.1')
const BOT_AUTH = 'offline';                    // 'offline' или 'microsoft'

// ---------- ЛОГИ ----------
function appendConnLog(line) {
  try {
    const file = path.join(__dirname, '..', 'logs', 'connection.log');
    const dir = path.dirname(file);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(file, `${new Date().toISOString()} ${line}\n`);
  } catch (e) {}
}

// ---------- ПАРСЕР NBT-СООБЩЕНИЙ ----------
function nbtToText(node) {
  if (node == null) return '';
  if (typeof node === 'string') return node;
  if (typeof node === 'number' || typeof node === 'boolean') return String(node);

  // mineflayer prismarine-nbt: { type, value }
  if (node.type && node.value !== undefined) {
    const v = node.value;
    if (node.type === 'string') return v;
    if (node.type === 'list' || node.type === 'array') {
      return (Array.isArray(v) ? v : []).map(nbtToText).join('');
    }
    if (node.type === 'compound') {
      // extra — массив частей сообщения
      if (v.extra) return nbtToText(v.extra);
      if (v.text !== undefined) return nbtToText(v.text);
      // на всякий случай — пройдёмся по всем полям
      return Object.values(v).map(nbtToText).join('');
    }
    return nbtToText(v);
  }

  if (Array.isArray(node)) return node.map(nbtToText).join('');
  if (typeof node === 'object') {
    if (node.extra) return nbtToText(node.extra);
    if (node.text !== undefined) return nbtToText(node.text);
    return Object.values(node).map(nbtToText).join('');
  }
  return String(node);
}

// ---------- СОЗДАНИЕ БОТА ----------
let bot;
let chatWrapped = false;

function wrapChat() {
  if (chatWrapped) return;
  if (!bot || typeof bot.chat !== 'function') return;
  const origChat = bot.chat.bind(bot);
  bot.chat = function (message) {
    try {
      if (typeof message === 'string') message = message.replace(/^\/s3\b/i, '/bw');
    } catch (e) {}
    return origChat(message);
  };
  chatWrapped = true;
}

function createBot() {
  chatWrapped = false;

  console.log(chalk.gray(`[LoveBot] Connecting to ${SERVER_HOST}:${SERVER_PORT} (version=${BOT_VERSION}, auth=${BOT_AUTH})...`));

  bot = mineflayer.createBot({
    host: SERVER_HOST,
    port: SERVER_PORT,
    username: 'дурной_порен',
    version: BOT_VERSION,
    auth: BOT_AUTH
  });

  wrapChat();

  bot.on('login', () => {
    console.log(chalk.green('[LoveBot] Logged in as LoveBot'));
    try { appendConnLog(`[LoveBot LOGIN] ${SERVER_HOST}:${SERVER_PORT}`); } catch (e) {}
    wrapChat();
  });

  bot.on('spawn', () => {
    console.log(chalk.green('[LoveBot] Spawned in world'));
    wrapChat();

    setTimeout(() => {
      try {
        if (typeof bot.chat === 'function') {
          bot.chat('/bw');
          console.log(chalk.gray('[LoveBot] Sent /bw after spawn'));
          try { appendConnLog(`[LoveBot] Sent /bw after spawn`); } catch (e) {}
        }
      } catch (e) {}
    }, 2000);

    setTimeout(() => {
      sendPartyInvite('after spawn');
    }, 4000);
  });

  bot.on('message', (jsonMsg, position) => {
    const text = jsonMsg.toString();
    if (!text || !text.trim()) return;
    const prefix = position === 'chat' ? '[Chat]' : position === 'system' ? '[System]' : '[Game]';
    console.log(chalk.white(`${prefix} ${text}`));

    if (/истекло/i.test(text) && /Party|Пати/i.test(text) && text.includes(PARTY_TARGET)) {
      console.log(chalk.yellow('[LoveBot] Party invite expired — resending /party...'));
      sendPartyInvite('invite expired');
      return;
    }

    if (/приглашени/i.test(text) && /Party|Пати/i.test(text) && text.includes(PARTY_TARGET)) {
      console.log(chalk.gray('[LoveBot] Saw party-related message about target.'));
    }
  });

  bot.on('title', (text) => {
    if (text) console.log(chalk.magenta('[Title]'), text);
  });

  bot.on('actionBar', (jsonMsg) => {
    const text = jsonMsg.toString();
    if (text && text.trim()) console.log(chalk.gray('[ActionBar]'), text);
  });

  bot.on('kicked', (reason) => {
    let readable = '';
    try { readable = nbtToText(reason); } catch (e) { readable = String(reason); }
    console.log(chalk.red('[LoveBot] Kicked:'), readable || JSON.stringify(reason));
    try { appendConnLog(`[LoveBot KICKED] ${readable || JSON.stringify(reason)}`); } catch (e) {}
  });

  bot.on('end', (reason) => {
    console.log(chalk.yellow(`[LoveBot] Disconnected: ${reason}. Reconnecting in 5s...`));
    try { appendConnLog(`[LoveBot END] ${reason}`); } catch (e) {}
    setTimeout(() => {
      try { createBot(); } catch (e) {
        console.log(chalk.red('[LoveBot] Reconnect failed:'), e.message || e);
      }
    }, 5000);
  });

  bot.on('error', (err) => {
    console.log(chalk.red('[LoveBot] Error:'), err && err.message ? err.message : err);
  });

  return bot;
}

// ---------- ОТПРАВКА ПРИГЛАШЕНИЯ ----------
function sendPartyInvite(reason) {
  const doSend = () => {
    try {
      if (typeof bot.chat === 'function') {
        bot.chat(PARTY_COMMAND);
        console.log(chalk.green(`[LoveBot] Sent ${PARTY_COMMAND} (${reason})`));
        try { appendConnLog(`[LoveBot] Sent ${PARTY_COMMAND} (${reason})`); } catch (e) {}
        return true;
      }
    } catch (e) {
      console.log(chalk.yellow('[LoveBot] Failed to send /party:'), e.message || e);
    }
    return false;
  };

  if (doSend()) return;

  console.log(chalk.gray('[LoveBot] chat not ready, waiting for spawn to send /party...'));
  bot.once('spawn', () => {
    setTimeout(doSend, 1000);
  });
}

// ---------- КОНСОЛЬ ----------
const rl = readline.createInterface({ input: process.stdin, output: process.stdout, prompt: chalk.gray('LoveBot> ') });
rl.prompt();
rl.on('line', (line) => {
  const t = (line || '').trim();
  if (!t) { rl.prompt(); return; }
  try {
    if (t.toLowerCase().startsWith('/send ')) {
      const msg = t.slice(6).trim();
      if (msg) { bot.chat(msg); console.log(chalk.green('[LoveBot] Sent:'), msg); }
    } else if (t.toLowerCase() === '/party') {
      sendPartyInvite('manual console');
    } else {
      bot.chat(t);
      console.log(chalk.green('[LoveBot] Sent:'), t);
    }
  } catch (e) {
    console.log(chalk.yellow('[LoveBot] Failed to send:'), e.message || e);
  }
  rl.prompt();
});
rl.on('close', () => { process.exit(0); });

// ---------- СТАРТ ----------
createBot();
console.log(chalk.gray('[LoveBot] Ready.'));

process.on('SIGINT', () => {
  console.log(chalk.yellow('\n[LoveBot] Shutting down...'));
  try { bot.quit(); } catch (_) {}
  process.exit(0);
});