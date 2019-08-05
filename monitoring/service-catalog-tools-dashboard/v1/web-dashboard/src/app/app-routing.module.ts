import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ListLaunchesComponent} from "./list-launches/list-launches.component";
import {ShowPipelinesComponent} from "./show-pipelines/show-pipelines.component";

const routes: Routes = [
  {
    path: '',
    redirectTo: '/list-launches',
    pathMatch: 'full'
  },
  {
    path: 'list-launches',
    component: ListLaunchesComponent
  },
  {
    path: 'show-pipelines',
    component: ShowPipelinesComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {useHash: true})],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
