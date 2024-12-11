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
  
    const postData: any = {
      content: data.content,
      user: user.id,
    };
  
    if (data.reservationId) {
      postData['reservationId'] = data.reservationId;  
    }
  
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

  deletePost(postId: number): Observable<any> {
    const user = this.authService.getUser();
  
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });
  
    return this.http
      .delete(`${this.api_url}post/${postId}/`, { headers })
      .pipe(
        catchError((error) => {
          console.error('Error deleting post:', error);
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

  createReservation(data:any):Observable<any> {
    let user = this.authService.getUser();

    const reservationData = {
      data: data,
      user: user.id
    };

    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });

    return this.http
      .post(`${this.api_url}reservation/`, data, { headers })
      .pipe(catchError((error) => throwError(error)));
  }
  
  getAllReservations():Observable<any> {
    let user = this.authService.getUser();

    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });

    return this.http
      .get(`${this.api_url}reservations/`, { headers })
      .pipe(catchError((error) => throwError(error)));
  }

  joinReservation(reservationId: number): Observable<any> {
    let user = this.authService.getUser();
  
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });
  
    return this.http
      .post(`${this.api_url}reservation/${reservationId}/join/`, {}, { headers })
      .pipe(
        catchError((error) => {
          console.error('Error joining reservation:', error);
          return throwError(error);
        })
      );
  }

  getUserReservations(reservationId?: number): Observable<any> {
    let user = this.authService.getUser();

    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });

    if (reservationId) {
      return this.http.get(`${this.api_url}reservation/${reservationId}/`, { headers })
        .pipe(catchError((error) => throwError(error)));
    }

    return this.http.get(`${this.api_url}reservation/`, { headers })
      .pipe(catchError((error) => throwError(error)));
  }

  deleteReservation(reservationId: number): Observable<any> {
    const user = this.authService.getUser();
  
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });
  
    return this.http
      .delete(`${this.api_url}reservation/${reservationId}/`, { headers })
      .pipe(
        catchError((error) => {
          console.error('Error deleting reservation:', error);
          return throwError(error);
        })
      );
  }

  updateReservation(reservationId: number, data: any): Observable<any> {
    const user = this.authService.getUser();
  
    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });
  
    return this.http
      .put(`${this.api_url}reservation/${reservationId}/`, data, { headers })
      .pipe(
        catchError((error) => {
          console.error('Error updating reservation:', error);
          return throwError(error);
        })
      );
  }


  getJoinedReservations(): Observable<any> {
    const user = this.authService.getUser();

    const headers = new HttpHeaders({
      'Authorization': `Token ${user.token}`,
      'Content-Type': 'application/json'
    });

    return this.http
      .get(`${this.api_url}reservations/joined/`, { headers })
      .pipe(
        catchError((error) => {
          console.error('Error fetching joined reservations:', error);
          return throwError(error);
        })
      );
    }

    leaveReservation(reservationId: number): Observable<any> {
      const user = this.authService.getUser();  
    
      const headers = new HttpHeaders({
        'Authorization': `Token ${user.token}`,  
        'Content-Type': 'application/json'  
      });
    
      return this.http
        .post(`${this.api_url}reservation/${reservationId}/leave/`, {}, { headers })
        .pipe(
          catchError((error) => {
            console.error('Error leaving reservation:', error);  
            return throwError(error);  
          })
        );
    }

    removeParticipantFromReservation(reservationId: number, userId: number): Observable<any> {
      const user = this.authService.getUser();
    
      const headers = new HttpHeaders({
        'Authorization': `Token ${user.token}`,
        'Content-Type': 'application/json'
      });
    
      return this.http
        .delete(`${this.api_url}reservation/${reservationId}/participant/${userId}/remove/`, { headers })
        .pipe(
          catchError((error) => {
            console.error('Error removing participant from reservation:', error);
            return throwError(error);
          })
        );
    }
}
