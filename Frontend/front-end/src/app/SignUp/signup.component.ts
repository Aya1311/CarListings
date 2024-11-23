//signmup.component.ts
import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../services';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  private apiUrl = 'http://localhost:8000/mycar/client/signup/';

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) {}

  onSubmit(form: NgForm) {
    if (form.valid) {
      const clientData = { 
        user: {
          username: form.value.username,
          email: form.value.email,
          password: form.value.password
        },
        age: form.value.age,
        budget_min: form.value.budget_min,
        budget_max: form.value.budget_max,
        boite_preferee: form.value.boite_preferee,
        carburant_prefere: form.value.carburant_prefere,
        role: 'client'
      };

      this.http.get('http://localhost:8000/mycar/get-csrf-token/').subscribe((response: any) => {
        const csrfToken = response.csrfToken;

        this.authService.createClient(clientData, csrfToken).subscribe(
          response => {
            this.router.navigate(['/login']);
          },
          error => {
            console.error('Erreur d\'inscription:', error);
          }
        );
      });
    }
  }
}
