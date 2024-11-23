//login.component.ts
import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../services';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  private loginUrl = 'http://localhost:8000/mycar/login/'; 

  constructor(private router: Router, private http: HttpClient, private authService: AuthService) {}

  onSubmit(form: NgForm) {
    if (form.valid) {
      const loginData = {
        username: form.value.username,
        password: form.value.password
      };

      // Obtenir le token CSRF
      this.http.get('http://localhost:8000/mycar/get-csrf-token/').subscribe((response: any) => {
        const csrfToken = response.csrfToken;

        this.authService.login(loginData, csrfToken).subscribe(
          (response: any) => {
            // Gestion des erreurs
            if (response.error) {
              console.error('Erreur de connexion:', response.error);
              return;
            }

            // La réponse peut inclure un redirection URL ou des messages
            if (response.redirectUrl) {
              window.location.href = response.redirectUrl; // Redirection en fonction de la réponse de Django
            }
          },
          (error) => {
            console.error('Erreur de connexion:', error);
          }
        );
      });
    }
  }

  redirectToSignup() {
    this.router.navigate(['/signup']);
  }
}
