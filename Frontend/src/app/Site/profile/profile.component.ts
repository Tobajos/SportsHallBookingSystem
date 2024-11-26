import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {

  userReservations: any[] = [];

  constructor(private siteService: SiteService) { }

  ngOnInit(): void {
    this.siteService.getUserReservations().subscribe(
      (reservations) => {
        this.userReservations = reservations;
        console.log("User reservations:", this.userReservations);
      },
      (error) => {
        console.error("Error fetching user reservations:", error);
      }
    );
  }
}
