import { Component } from '@angular/core';
import { AuthService } from '../../Services/auth.service';
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  constructor(private authService: AuthService, private router: Router) {}

  errorMessage: string | null = null; 

  onSubmit(form: NgForm) {
    const data = {
      "email": form.value.email,
      "password": form.value.password
    };

    this.authService.login(data).subscribe(
      (response: any) => {
        localStorage.setItem('User', JSON.stringify({
          "user_id": response.user_id,
          "email": response.email,
          "token": response.token,
          "firstname": response.firstname,
          "lastname": response.lastname,
          "is_staff": response.is_staff
        }));
        this.router.navigate(['/']);
      },
      error => {
        this.errorMessage = error.error.message || 'Login failed. Please try again.';
        console.log(error.error);
      }
    );
  }
}
