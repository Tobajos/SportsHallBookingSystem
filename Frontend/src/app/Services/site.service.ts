import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SiteService {

  private api_url = "http://localhost:8000/bookingapi/";

  constructor(private http:HttpClient, private authService: AuthService) { }

  getPosts():Observable<any>{
    let user = this.authService.getUser();

    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`
    });
    console.log("Authorization header:", `Token ${user.token}`);

    return this.http.get(`${this.api_url}posts`, { headers }).pipe(
      catchError(error => {
        return throwError(error);
      })
    );
  }
}
