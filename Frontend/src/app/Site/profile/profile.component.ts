import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';
import { faTrash,faBars } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {

  edit = faBars
  delete = faTrash;
  userReservations: any[] = [];
  selectedReservationId: number | null = null;
  isConfirmationVisible: boolean = false;
  editingReservationId: number | null = null;
  editingData: any = {};


  constructor(private siteService: SiteService) { }

  ngOnInit(): void {
    this.loadReservations();
  }

  loadReservations(): void {
    this.siteService.getUserReservations().subscribe(
      (reservations) => {
        this.userReservations = reservations;
        console.log('User reservations:', this.userReservations);
      },
      (error) => {
        console.error('Error fetching user reservations:', error);
      }
    );
  }

  deleteReservation(reservationId: number): void {
    this.siteService.deleteReservation(reservationId).subscribe(
      (response) => {
        console.log('Reservation deleted successfully:', response);
        
        this.loadReservations();
      },
      (error) => {
        console.error('Error deleting reservation:', error);
      }
    );
  }

  showConfirmation(reservationId: number): void {
    this.selectedReservationId = reservationId;
    this.isConfirmationVisible = true;
  }
  
  hideConfirmation(): void {
    this.selectedReservationId = null;
    this.isConfirmationVisible = false;
  }
  
  confirmDelete(): void {
    if (this.selectedReservationId !== null) {
      this.deleteReservation(this.selectedReservationId);
      this.hideConfirmation();
    }
  }
  startEdit(reservation: any): void {
    this.editingReservationId = reservation.id;
    this.editingData = { ...reservation }; 
  }
  
  cancelEdit(): void {
    this.editingReservationId = null;
    this.editingData = {};
  }
  
  saveReservation(reservationId: number): void {
    if (this.editingReservationId) {
      this.siteService.updateReservation(reservationId, this.editingData).subscribe(
        (response) => {
          console.log('Reservation updated successfully:', response);
          this.loadReservations(); 
          this.cancelEdit(); 
        },
        (error) => {
          console.error('Error updating reservation:', error);
        }
      );
    }
  }
  
}
