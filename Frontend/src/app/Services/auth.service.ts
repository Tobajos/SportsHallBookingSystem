import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private api_url = "http://localhost:8000/auth/"

  constructor(private http: HttpClient) { }

  setHeaders(){
    let headers = new HttpHeaders();
    let user = this.getUser()
    
    if (user && user.token) {
      headers = headers.set('Authorization', `Token ${user.token}`);
    }
    return headers
  }

  getUser() {
    const userString = localStorage.getItem('User');
    return userString ? JSON.parse(userString) : null;
  }

  login(data:any){
    return this.http.post(`${this.api_url}login/`,data);
  }

  register(data:any){
    return this.http.post(`${this.api_url}register/`,data)
  }

  Logout(){
    let user = this.getUser();
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`
    });
    return this.http.post(`${this.api_url}logout/`,null, {headers})
  }
}
