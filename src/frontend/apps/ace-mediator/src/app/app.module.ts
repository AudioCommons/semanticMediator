import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

//https://blog.angular-university.io/introduction-to-angular-2-forms-template-driven-vs-model-driven/
//import { FormsModule } from '@angular/forms'; //for the 'Template Driven Forms'
import {ReactiveFormsModule} from "@angular/forms"; //for the 'Reactive Forms' i.e. 'Model Driven Forms'

import { FlexLayoutModule } from '@angular/flex-layout';

import { HttpClientModule }    from '@angular/common/http';

// Material
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import 'hammerjs';
import {MaterialModule} from './materialModule';
// import { OrderModule } from 'ngx-order-pipe'; //TODO
//import {MatInputModule, MatFormFieldControl} from '@angular/material';

import { ColaboFlowAuditModule } from '@colabo-flow/f-audit';
import {IndexComponent} from './index/index.component';
import { UtilsNotificationModule, UtilsNotificationService } from '@colabo-utils/f-notifications';

//import {ModerationPanelComponent} from '@colabo-moderation/f-core';

import { AppComponent } from './app.component';

import { AppRoutingModule } from './app-routing.module';


var moduleDeclarations = [
  AppComponent,
  IndexComponent
];

var moduleImports = [
  BrowserModule
  , HttpClientModule
  //,FormsModule,
  ,ReactiveFormsModule

  // Material
  , BrowserAnimationsModule
  , MaterialModule
  , FlexLayoutModule
  , AppRoutingModule
  // , OrderModule
  // ,
  // MatInputModule,
  // MatFormFieldControl

  // Puzzle modules
  , UtilsNotificationModule
  , ColaboFlowAuditModule
];
// moduleImports.push(MainModule);

moduleImports.push(AppRoutingModule);

// import {GlobalEmitterService} from '@colabo-puzzles/f-core/code/puzzles/globalEmitterService';
import {GlobalEmittersArrayService} from '@colabo-puzzles/f-core/code/puzzles/globalEmitterServicesArray';

declare var window:any;

// old external way of declaring puzzles' config
// export var Plugins:any = window.Config.Plugins;

@NgModule({
  declarations: moduleDeclarations,
  imports: moduleImports,
  entryComponents: [
  ],
  providers: [
    UtilsNotificationService,

    // old external way of injecting puzzles' config
    // through Plugins service
    // {provide: "Plugins", useValue: Plugins},

    // provide ng build error: "Can't resolve all parameters for GlobalEmitterService"
    // {provide: GlobalEmitterService, useClass: GlobalEmitterService},
    {provide: GlobalEmittersArrayService, useClass: GlobalEmittersArrayService},
    // TODO: move out of here, into puzzles' modules
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
