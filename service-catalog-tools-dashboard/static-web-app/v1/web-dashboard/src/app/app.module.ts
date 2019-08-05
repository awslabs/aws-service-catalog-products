import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {ListLaunchesComponent} from './list-launches/list-launches.component';

import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HeaderComponent} from './header/header.component';
import {FooterComponent} from './footer/footer.component';
import {HeaderInterceptor} from "./_helpers";
import {ShowPipelinesComponent} from './show-pipelines/show-pipelines.component';
import {SpinnerComponent} from './spinner/spinner.component';


@NgModule({
  declarations: [
    AppComponent,
    ListLaunchesComponent,
    HeaderComponent,
    FooterComponent,
    ShowPipelinesComponent,
    SpinnerComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [
    {provide: HTTP_INTERCEPTORS, useClass: HeaderInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
