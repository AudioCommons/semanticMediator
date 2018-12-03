'use strict';

// this is file is available to the rest of the system
// through the puzzle `@colabo-utils/i-config`
// please read `@colabo-utils/i-config/README.md` for more details

// NOTE: it is important that this file is not imported, but required
// and that it is therefore JS (not TS, although it can be, if we still do not import it)
// because otherwise it would be bundled in a final file during building
// and we wouldn't be able to change the config after building project

console.log("[config/global.js] Setting up the globalSet variable");

let globalSet = {};
if (typeof window !== 'undefined' && typeof window !== 'null') {
    if (!window.hasOwnProperty('globalSet')) window.globalSet = {};
    globalSet = window.globalSet;
}
if (typeof global !== 'undefined' && typeof global !== 'null') {
    if (!global.hasOwnProperty('globalSet')) global.globalSet = {};
    globalSet = global.globalSet;
}

console.log("[config/global.js] Populating the globalSet variable");

if (!globalSet.hasOwnProperty('general')) {
    console.log("[config/global.js] Setting up globalSet.general");
    globalSet.general = {
        // RESTfull backend API url
        serverUrl: 'http://127.0.0.1:6001', // LOCAL
        // 'https://fv.colabo.space/api', // colabo-space-1 (https) (ACTUAL SERVER)
        //OLD:
        // 'http://api.colabo.space',
        // 'http://158.39.75.120:6001', // colabo-space-1 (old)

        imagesFolder: 'images',

        // active map
        mapId: '5be3fddce1b7970d8c6df406',
        mapIdSDGs: '5be3fddce1b7970d8c6df406',
        userNodeId: '5be408d0e1b7970d8c6df40f',

        lang: 'en',
        //'rs',

        /** multiple players can play on the same opening card */
        OPENNING_CARD_MULTIPLE_ANSWERS: true,

        /** multiple players can play on a card played by another player */
        PLAYER_CARD_MULTIPLE_ANSWERS: true,

        /** multiple players can play on a card played by another player */
        REPLAY_PLAYED_CARD: false
    };
}

if (!globalSet.hasOwnProperty('puzzles')) {
    console.log("[config/global.js] Setting up globalSet.puzzles");
    globalSet.puzzles = {
        '@colabo-topichat/f-core': {
            // socketUrl: 'http://localhost/',
            socketUrl: 'http://localhost:6001/',
            // socketUrl: 'https://fv.colabo.space/',
            path: '',
            // path: '/api/socket.io'
        },
        '@colabo-topichat/f-talk': {
            messagesNumberMin: 3,
            messagesNumberMax: 5
        }
    };
}

console.log("[config/global.js] globalSet.puzzles:", globalSet.puzzles);

// node support (export)
if (typeof module !== 'undefined') {
    // workarround for TypeScript's `module.exports` readonly
    if ('exports' in module) {
        if (typeof module['exports'] !== 'undefined') {
            module['exports'].globalSet = globalSet;
        }
    } else {
        module['exports'] = globalSet;
    }
}

console.log("[config/global.js] finished");