import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PythonComponent } from './python/python.component';

const routes: Routes = [
  { path: 'game', component: PythonComponent},
  { path: '', redirectTo: 'game', pathMatch: 'full'},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
