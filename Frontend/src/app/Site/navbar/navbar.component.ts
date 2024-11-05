import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../../Services/auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy {
  user: any; 
  private subscription: Subscription = new Subscription(); 

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.subscription = this.authService.user$.subscribe(user => {
      this.user = user; 
    });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe(); 
  }

  logout() {
    this.authService.logout().subscribe(() => {
      
    });
  }
}
