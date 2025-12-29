const fs = require('fs');
const jwt = require('jsonwebtoken');

// Fill in these from Apple Developer Center
const TEAM_ID = '3C2UHTV9QT';
const KEY_ID = 'WYZ54N72VU';
const CLIENT_ID = 'com.sciencefair.appleoxidation.service';

// Read your p8 file
const privateKey = fs.readFileSync('/Users/andrew/Downloads/AuthKey_QG4929VZBH.p8', 'utf8');

// Generate JWT
const payload = {
  iss: TEAM_ID,
  aud: 'https://appleid.apple.com',
  sub: CLIENT_ID,
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + 86400 * 180 // 180 days
};

const token = jwt.sign(payload, privateKey, { algorithm: 'ES256', header: { kid: KEY_ID } });

console.log('Your Apple JWT:');
console.log(token);
