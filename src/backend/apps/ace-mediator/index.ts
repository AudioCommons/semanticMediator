const MODULE_NAME:string = "@colabo-apps/b-colabo-space";

// let chalk = require('chalk');
import chalk from 'chalk'

let AppNameText = chalk.yellow.bold("ACE")+chalk.blue.bold("-Mediator")+chalk.white.bold(" Backend");
console.log(AppNameText + " is starting ...")

process.chdir(__dirname);

// import * as express from "express";

let configFile:any = require('./config/global');
let globalSet:any = configFile.globalSet;
console.log("[Colabo.Space:index] globalSet.paths: %s", JSON.stringify(globalSet.paths));
let config = require('@colabo-utils/i-config');
config.init(globalSet);

let async = require('async');
let express = require('express');
let resource = require('express-resource');
let fs = require('fs');
let http = require('http');
let https = require('https');

function supportCrossOriginScript(req, res, next) {
    res.header("Access-Control-Allow-Headers", "Content-Type");

    // res.header("Access-Control-Allow-Headers", "Origin");
    // res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    // res.header("Access-Control-Allow-Methods","POST, OPTIONS");
    res.header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT, HEAD");
    res.header("Allow", "POST, GET, OPTIONS, DELETE, PUT, HEAD");
    // res.header("Access-Control-Max-Age","1728000");

    // res.header("Access-Control-Allow-Origin", "*");
    // http://stackoverflow.com/questions/15026016/set-cookie-in-http-header-is-ignored-with-angularjs
    var origin = req.headers.origin; // "litterra.info"; // "litterra.info:8088"; //req.headers.origin;

    //console.log("Access-Control-Allow-Origin: %s", origin);

    //var ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    // console.log("Access-Control-Allow-Origin: %s", ip);

    //console.log("Access-Control-Allow-Origin: %s", origin);

    res.header('Access-Control-Allow-Origin', origin);
    res.header('Access-Control-Allow-Credentials', true);

    //console.log("[supportCrossOriginScript] setting up headers");

    res.status(200);
    next();
}

var portHttp = process.argv[2] || process.env.PORT || 8888;

var expressApp = express();

var morgan = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

// exported in v4.*
// expressApp.use(express.logger());
expressApp.use(morgan('combined'));
// exported in v4.*
// expressApp.use(express.cookieParser()); // cookie parser is used before the session
expressApp.use(cookieParser());

// multer and body-parser resolution
// https://github.com/expressjs/multer/issues/251

// parse application/x-www-form-urlencoded
// note this might conflict with multer, it was with express v3.* probably not any more with v4.*
expressApp.use(bodyParser.urlencoded({ extended: false }));
// expressApp.use(express.urlencoded());

// parse application/json
// note this might conflict with multer, it was with express v3.* probably not any more with v4.*
expressApp.use(bodyParser.json());
// expressApp.use(express.json());

console.log("process.argv: %s", JSON.stringify(process.argv));
expressApp.set('port', portHttp);

expressApp.use(supportCrossOriginScript);
// not used anymore in v4.*
// expressApp.use(expressApp.router);

import * as ColaboFlowAudit from '@colabo-flow/b-audit';
ColaboFlowAudit.initialize(expressApp);

// let server = http.createServer(expressApp).listen(expressApp.get('port')
let httpServer = http.Server(expressApp);
httpServer.listen(portHttp, function () {
    console.log('%s is listening on the %s', AppNameText, chalk.bold.blue('*:'+portHttp));
});

console.log(AppNameText + " started ...")
