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

  createPost(data: any): Observable<any> {
    let user = this.authService.getUser();  
  
    
    const postData = {
      content: data,  
      user: user.id   
    };
  
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,  
      'Content-Type': 'application/json'       
    });
  
    return this.http.post(`${this.api_url}post/`, postData, { headers }).pipe(
      catchError(error => {
        return throwError(error);
      })
    );
  }

  createComment(postId: number, content: string): Observable<any> {
    let user = this.authService.getUser();

    const commentData = {
      content: content,
      user: user.id
    };

    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });

    return this.http.post(`${this.api_url}post/${postId}/comments/`, commentData, { headers }).pipe(
      catchError(error => {
        return throwError(error);
      })
    );
  }

  getCommentsForPost(postId: number): Observable<any> {
    const user = this.authService.getUser();
    
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });
  
    return this.http.get(`${this.api_url}post/${postId}/comments/`, { headers }).pipe(
      catchError(error => {
        return throwError(error);
      })
    );
  }
}
