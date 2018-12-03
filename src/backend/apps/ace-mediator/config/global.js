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

console.log("Setting up the global variable");

if (!globalSet.hasOwnProperty('general')) {
    console.log("[config/global.js] Setting up globalSet.general");
    globalSet.general = {
        // active map
        // mapId: '5b96619b86f3cc8057216a03',
    };
}

var path = require('path');

// expose this function to our app using module.exports
if (!globalSet.hasOwnProperty('paths')) {
    console.log("Setting up globalSet.paths");
    globalSet.paths = {};
    globalSet.paths.DATASET_FOLDER = path.resolve(globalSet.paths.EXPERIMENTS_FOLDER + "/data");
    globalSet.paths.FOLDER_OUT = path.resolve(globalSet.paths.DATASET_FOLDER + "/out");
    globalSet.paths.FOLDER_CACHE = path.resolve(globalSet.paths.EXPERIMENTS_FOLDER + "/cache");
}

if (!globalSet.hasOwnProperty('dbConfig')) {
    console.log("Setting up globalSet.dbConfig");
    globalSet.dbConfig = {
        newConnect: true,
        dbName: "KnAllEdge",
        domain: '127.0.0.1',
        port: 27017,
        user: 'user',
        pass: 'pass'
    };
}

if (!globalSet.hasOwnProperty('puzzles')) {
    console.log("Setting up globalSet.puzzles");
    globalSet.puzzles = {
        '@colabo-topichat/b-core': {
            debug: false
        },
        '@colabo-topichat/b-talk': {
            saveTalkToMap: false,
            emitMessages: true,
            mapId: "5be3fddce1b7970d8c6df406",
            iAmId: "1b96619b86f3cc8057216a05",
            nodeId: ""
        },
        '@colabo-topichat/b-clients-orchestration': {
            saveTalkToMap: true,
            emitMessages: true,
            emitMessagesToSender: true,
            mapId: "5be3fddce1b7970d8c6df406",
            iAmId: "1b96619b86f3cc8057216a05",
            nodeId: ""
        },
        '@colabo-flow/b-services': {
            debug: true,

            // https://www.rabbitmq.com/uri-spec.html
            // amqp://user:pass@host.com:port/vhost
            // url: 'amqp://guest:guest@localhost:5672',
            // url: 'amqp://colabo:colabo_usr56@158.39.75.31:5672',
            url: 'amqp://localhost:5672',
            cancelCunsumerTags: false,
            // queue: 'colabo-service',
            queue: 'colabo-service-localhost',

            shouldRequestResult: true,
            noAck: true,

            shouldListenOnSeparateResponseQueue: false,
            separateResponseQueue: 'colabo-service-response'
                // separateResponseQueue: 'colabo-service-response-localhost'
        },
        '@colabo-flow/b-topichat': {
            saveFlowInteractionToMap: true,
            mockupQueueAccess: false,
            mapId: "5be3fddce1b7970d8c6df406"
        },
        '@colabo-media/b-upload': {
            tmpUpload: '/tmp/uploads',
            imagesFolder: '/tmp/images'
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