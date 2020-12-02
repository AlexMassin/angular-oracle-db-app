import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { QueryComponent } from './query/query.component';
import { ManualQueryComponent } from './manual-query/manual-query.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'query', component: QueryComponent },
  { path: 'manual-query', component: ManualQueryComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }