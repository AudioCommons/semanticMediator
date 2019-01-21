const MODULE_NAME: string = "@ace-mediator/service-check-credentials";

let chalk = require('chalk');
let coLaboFlowAuditText = chalk.red("Colabo") + chalk.blue("Flow") + "Go - check-credentials @ ACE Service";
console.log(coLaboFlowAuditText + " is starting ...")

process.chdir(__dirname);

// import * as express from "express";

import { ColaboFlowGoActionHostServer } from '@colabo-flow/s-go';
import { RpcMethods, RpcCallback, ActionExecuteRequestInterface, ActionExecuteReply } from '@colabo-flow/i-go';

import { init, GetProperty, GetPuzzle } from '@colabo-utils/i-config';
const configFile: any = require('./config/global');
const globalSet: any = configFile.globalSet;
console.log("[ColaboFlow.Go:index] globalSet.paths: %s", JSON.stringify(globalSet.paths));
init(globalSet);
const puzzleConfig: any = GetPuzzle(MODULE_NAME);
const dbConfigPostgres: any = GetProperty('dbConfigPostgres');


const fs = require('fs');

const { Pool, Client } = require('pg')

const pool = new Pool(dbConfigPostgres);

var _ACTION_EXECUTION_ID:number = 0;

enum SupportedActions{
    CheckAuthorization = 'check-authorization'
}

const queryUsers = {
    // give the query a unique name
    name: 'fetch-users',
    text: 'SELECT * FROM accounts_account WHERE is_active = $1',
    values: [true]
}

function checkAuthorization(actionExecuteRequestInterface: ActionExecuteRequestInterface, callback: RpcCallback) {
    // promise
    pool.query(queryUsers)
        .then(res => {
            console.log(res.rows)
            let actionExecuteReply: ActionExecuteReply = {
                id: "" + _ACTION_EXECUTION_ID,
                dataOut: JSON.stringify(res.rows),
                params: "All is well!",
                error: null
            };
            console.log("actionExecuteReply: %s", JSON.stringify(actionExecuteReply));
            callback(null, actionExecuteReply);
        })
        .catch(e => {
            console.error(e.stack);
            let actionExecuteReply: ActionExecuteReply = {
                id: "" + _ACTION_EXECUTION_ID,
                dataOut: "Hello from check-credentials",
                params: "All is well!",
                error: JSON.stringify(e)
            };
            console.error("[error] actionExecuteReply: %s", JSON.stringify(actionExecuteReply));
            callback(null, actionExecuteReply);
        })
}

function executeAction(actionExecuteRequestInterface: ActionExecuteRequestInterface, callback: RpcCallback){
    console.log("actionExecuteRequestInterface: %s", JSON.stringify(actionExecuteRequestInterface));
    
    switch (actionExecuteRequestInterface.name){
        case SupportedActions.CheckAuthorization:
            checkAuthorization(actionExecuteRequestInterface, callback);
            break;
        default:
            console.error("Unsupported action: %s", actionExecuteRequestInterface.name);
            let actionExecuteReply: ActionExecuteReply = {
                id: "" + _ACTION_EXECUTION_ID,
                dataOut: "Hello from check-credentials",
                params: "",
                error: "Unsupported action: " + actionExecuteRequestInterface.name
            };
            callback(null, actionExecuteReply);
            break;
    }
    
    _ACTION_EXECUTION_ID += 1;
}

let rpcMethods: RpcMethods = {
    executeAction: executeAction.bind(this)
}

let colaboFlowGoActionHostServer = new ColaboFlowGoActionHostServer();
colaboFlowGoActionHostServer.init(rpcMethods);
colaboFlowGoActionHostServer.start();
console.log(coLaboFlowAuditText + " started ...");