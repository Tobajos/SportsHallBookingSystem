import { Component, OnDestroy, OnInit, HostListener } from '@angular/core';
import { AuthService } from '../../Services/auth.service';
import { Subscription } from 'rxjs';
import { faUser } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy {
  userIcon = faUser;
  user: any; 
  dropdownVisible: boolean = false; 
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

  toggleDropdown() {
    this.dropdownVisible = !this.dropdownVisible;
  }

  @HostListener('document:click', ['$event'])
  handleClickOutside(event: Event) {
    const target = event.target as HTMLElement;
    if (!target.closest('.dropdown')) {
      this.dropdownVisible = false;
    }
  }

  logout() {
    this.authService.logout().subscribe(() => {
      this.user = null;
    });
  }
}
