const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// SECRET - only you know this, not in the script
const SECRET = "IRISH_HUB_SECRET_2024_X9K2";
const NUM_KEYS = 500;
const CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

function generateKey(index) {
    const hash = crypto.createHmac('sha256', SECRET).update(String(index)).digest('hex');
    // Take 12 chars from hash, map to charset (3 groups of 4)
    let key = "IRISH-";
    for (let i = 0; i < 12; i++) {
        if (i > 0 && i % 4 === 0) key += "-";
        const idx = parseInt(hash[i], 16) % CHARSET.length;
        key += CHARSET[idx];
    }
    return key;
}

function validateKey(key) {
    // Format check
    if (!/^IRISH-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(key)) return false;
    // Brute check: regenerate all and compare
    for (let i = 0; i < NUM_KEYS; i++) {
        if (generateKey(i) === key) return true;
    }
    return false;
}

// Generate all keys
const keys = [];
for (let i = 0; i < NUM_KEYS; i++) {
    keys.push(generateKey(i));
}

// Save keys list
fs.writeFileSync(path.join(__dirname, 'keys.txt'), keys.join('\n'));

// Save keys as compact JS array for web page
const keysJS = `const VALID_KEYS = ${JSON.stringify(keys)};\n`;
fs.writeFileSync(path.join(__dirname, 'keys_data.js'), keysJS);

console.log(`Generated ${NUM_KEYS} keys`);
console.log(`First 5: ${keys.slice(0, 5).join(', ')}`);
console.log(`Last: ${keys[keys.length - 1]}`);
console.log(`Validate test: ${validateKey(keys[0])} (should be true)`);
console.log(`Validate test: ${validateKey('IRISH-AAAA-BBBB-CCCC')} (should be false)`);
