import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private api_url = "http://localhost:8000/auth/";
  private userSubject = new BehaviorSubject<any>(this.getUser());
  public user$ = this.userSubject.asObservable(); 

  constructor(private http: HttpClient) { }

  getUser() {
    const userString = localStorage.getItem('User');
    return userString ? JSON.parse(userString) : null;
  }

  login(data: any): Observable<any> {
    return this.http.post(`${this.api_url}login/`, data).pipe(
      tap((response: any) => {
        console.log('to jest z authService',response); 
        localStorage.setItem('User', JSON.stringify(response)); 
        this.userSubject.next(response); 
      })
    );
  }
  
  

  register(data: any) {
    return this.http.post(`${this.api_url}register/`, data);
  }

  logout() {
    const user = this.getUser();
    const headers = new HttpHeaders({
      'Authorization': `Token ${user?.token}`
    });
    return this.http.post(`${this.api_url}logout/`, null, { headers }).pipe(
      tap(() => {
        localStorage.removeItem('User'); 
        this.userSubject.next(null); 
      })
    );
  }
}
