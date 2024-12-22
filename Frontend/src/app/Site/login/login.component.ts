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

  errorMessage: string | null = null; // Przechowywanie komunikatów o błędach

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
          "lastname": response.lastname
        }));
        this.router.navigate(['/']);
      },
      error => {
        // Ustaw wiadomość o błędzie na podstawie odpowiedzi backendu
        this.errorMessage = error.error.message || 'Login failed. Please try again.';
        console.log(error.error);
      }
    );
  }
}
