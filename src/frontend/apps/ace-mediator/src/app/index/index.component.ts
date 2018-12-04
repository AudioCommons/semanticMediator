import { Component, OnInit } from '@angular/core';
import { GetPuzzle, GetGeneral } from '@colabo-utils/i-config';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit {
  protected generalConfigBranding: any;

  constructor(
  ) {
    this.generalConfigBranding = GetGeneral('branding');
  }

  ngOnInit() {
  }

  get logo(): string {
    return this.generalConfigBranding.logo;
  }

  get isLoggedIn():boolean{
    return true;
  }

  get loggedUser(): any {
    return null;
  }

  logOut(){
  }

}
