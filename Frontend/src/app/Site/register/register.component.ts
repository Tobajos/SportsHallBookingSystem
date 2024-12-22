import { Component } from '@angular/core';
import { AuthService } from '../../Services/auth.service';
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(form: NgForm) {
    this.errorMessage = null;
    this.successMessage = null;

    const data = {
      email: form.value.email,
      password: form.value.password,
      firstname: form.value.firstname,
      lastname: form.value.lastname,
    };

    this.authService.register(data).subscribe(
      (response: any) => {
        this.successMessage = response.message; 
        setTimeout(() => this.router.navigate(['login']), 2000); 
      },
      (error) => {
        this.errorMessage = error.error.errors
          ? error.error.errors.join('. ')
          : 'Registration failed. Please try again.';
      }
    );
  }
}

