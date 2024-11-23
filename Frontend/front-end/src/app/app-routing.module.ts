//app-routing.module.ts
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './Login/login.component';
import { SignupComponent } from './SignUp/signup.component';
import { ClientDashboardComponent } from './ClientDashboard/client-dashboard.component';
import { CarDetailComponent } from './CarDetails/car-detail.component';
import { CompareComponent } from './Compare/compare.component';
import { SavedCarsComponent } from './SavedCars/saved-cars.component';
import { AdminDashboardComponent } from './AdminDashboard/admin-dashboard.component';


const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'dashboard_client/:id', component: ClientDashboardComponent },
  { path: 'car-detail/:id', component: CarDetailComponent },
  { path: 'compare/:car1Id/:car2Id', component: CompareComponent },
  { path: 'saved-cars/:id', component: SavedCarsComponent },
  { path: 'dashboard_admin/:id', component: AdminDashboardComponent },
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
