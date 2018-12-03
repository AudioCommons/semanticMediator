import { NgModule } from '@angular/core';
import { RouterModule, Routes} from '@angular/router';

import {IndexComponent} from './index/index.component';
import { ColaboFlowAuditForm } from '@colabo-flow/f-audit';

const routes: Routes = [
  { // default route
    path: '',
    pathMatch: 'full',
    component: IndexComponent
  },
  {
    path: 'colaboflow-audits',
    component: ColaboFlowAuditForm
  }
];

@NgModule({
  exports: [
    // makes router directives available for use in
    // other components that will need them
    RouterModule
  ],
  imports: [
    // initialize RouterModule with routes
    RouterModule.forRoot(routes)
  ]
})

export class AppRoutingModule { }
