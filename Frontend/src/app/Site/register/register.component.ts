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

  constructor(private authService: AuthService, private router:Router){}

  onSubmit(form:NgForm){

    let data ={
      "email": form.value.email,
      "password": form.value.password,
      "firstname": form.value.firstname,
      "lastname": form.value.lastname
    }

    this.authService.register(data).subscribe(
      (response: any)=>{
        this,this.router.navigate(['login'])
      },
      error => {
        console.error('Error', error.error)
      }
    )
  }
}
