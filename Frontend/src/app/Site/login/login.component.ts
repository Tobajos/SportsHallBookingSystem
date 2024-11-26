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

  constructor(private authService: AuthService, private router:Router ) {}

  user: any;
  
  onSubmit(form: NgForm){
    let data = {
      "email": form.value.email,
      "password": form.value.password
    }
    this.authService.login(data).subscribe(
      (response:any)=>{
        localStorage.setItem('User', JSON.stringify({
          "user_id":response.user_id,
          "email":response.email,
          "token":response.token,
          "firstname":response.firstname,
          "lastname": response.lastname

        }));
        this.router.navigate(['/'])
      },
      error =>{
        console.log(error.error)
      }
    )
  }
}
