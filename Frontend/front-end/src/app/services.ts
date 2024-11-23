//service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

// Service to get CSRF token from cookies
@Injectable({
  providedIn: 'root'
})
export class CsrfTokenService {
  getCsrfToken(): string | null {
    const name = 'csrftoken';
    const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name));
    return cookieValue ? cookieValue.split('=')[1] : null;
  }
}

// AuthService for user authentication
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private signupUrl = 'http://localhost:8000/mycar/client/signup/';
  private loginUrl = 'http://localhost:8000/mycar/login/';

  constructor(private http: HttpClient, private csrfTokenService: CsrfTokenService) {}

  createClient(clientData: any, csrfToken?: string): Observable<any> {
    const headers = new HttpHeaders().set('X-CSRFToken', csrfToken || '');
    return this.http.post(this.signupUrl, clientData, { headers });
  }

  login(loginData: any, csrfToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    });

    return this.http.post<any>(this.loginUrl, loginData, { headers });
  }
}

// CarService for handling car-related API requests
@Injectable({
  providedIn: 'root'
})

export class CarService {
  private apiUrl = 'http://127.0.0.1:8000/mycar/api'; 

  constructor(private http: HttpClient) {}

  getCars(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/car_data/`);
  }
  getCarDetails(carId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/car_details/${carId}/`).pipe(
      tap(data => console.log(`Détails de la voiture ${carId}:`, data))
    );

  }
  getSavedCars(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/saved_cars/${userId}/`);
  }

  recordVisit(userId: number, carId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/record_visit/${userId}/${carId}/`);
  }
  recordSave(userId: number, carId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/record_save/${userId}/${carId}/`);
  }
  getCarsCount(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/car_data/count/`); 
  }
  getRecommendedCars(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/recommended-cars/${userId}`);
  }
}
@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private listApiUrl = 'http://127.0.0.1:8000/mycar/admin/admin_list/';
  private createApiUrl = 'http://127.0.0.1:8000/mycar/admin/signup/';

  constructor(private http: HttpClient) { }

  getAdmins(): Observable<any[]> {
    return this.http.get<any[]>(this.listApiUrl);
  }

  createAdmin(username: string, email: string, password: string): Observable<any> {
    return this.http.post<any>(this.createApiUrl, {
      user: { username, email, password },
      role: 'admin'
    });
  }
}
@Injectable({
  providedIn: 'root'
})
export class ClientService {
  private apiUrl = 'http://127.0.0.1:8000/mycar/client/client_list';
  private countUrl = 'http://127.0.0.1:8000/mycar/client/count/'; 

  constructor(private http: HttpClient) { }

  getClients(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  getClientCount(): Observable<any> {
    return this.http.get<any>(this.countUrl);
  }
}