import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';  
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';
import { CommonModule } from '@angular/common';

// Composants
import { AppComponent } from './app.component';
import { SignupComponent } from './SignUp/signup.component';
import { LoginComponent } from './Login/login.component';
import { ClientDashboardComponent } from './ClientDashboard/client-dashboard.component';
import { CarDetailComponent } from './CarDetails/car-detail.component';
import { CompareComponent } from './Compare/compare.component';
import { SavedCarsComponent } from './SavedCars/saved-cars.component';
import { AdminDashboardComponent } from './AdminDashboard/admin-dashboard.component';
import { RecommendedCarsComponent } from './RecommendedCars/recommended-cars.component'; // Ajustez le chemin si nécessaire

// Services
import { CsrfTokenService } from './services'; 
import { AdminService } from './services'; 

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'dashboard_client/:id', component: ClientDashboardComponent },
  { path: 'car-detail/:id', component: CarDetailComponent },
  { path: 'compare/:car1Id/:car2Id', component: CompareComponent },
  { path: 'saved-cars/:id', component: SavedCarsComponent },
  { path: 'dashboard_admin/:id', component: AdminDashboardComponent },
  { path: 'recommended-cars/:id', component: RecommendedCarsComponent },

];

@NgModule({
  declarations: [
    AppComponent,
    SignupComponent,
    LoginComponent,
    ClientDashboardComponent,
    CarDetailComponent,
    CompareComponent,
    SavedCarsComponent,
    AdminDashboardComponent,
    RecommendedCarsComponent,
  ],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,  
    HttpClientModule,
    RouterModule.forRoot(routes),
  ],
  providers: [CsrfTokenService, AdminService],
  bootstrap: [AppComponent]
})
export class AppModule { }
