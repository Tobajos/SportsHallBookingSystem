import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';
import { AuthService } from '../../Services/auth.service';
import { faTrash, faBars, faRightFromBracket, faUserXmark } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  // FontAwesome icons
  kick = faUserXmark;
  leave = faRightFromBracket;
  edit = faBars;
  delete = faTrash;

  // Data
  userReservations: any[] = [];
  participantReservations: any[] = [];
  selectedReservationId: number | null = null;
  editingReservationId: number | null = null;
  editingData: any = {};
  isAdmin: boolean = false;

  // Modals and confirmations
  isConfirmationVisible: boolean = false;
  isLeaveConfirmationVisible: boolean = false;
  isParticipantRemoveConfirmationVisible: boolean = false;
  selectedParticipantId: number | null = null;
  selectedReservationForParticipant: number | null = null;

  constructor(private siteService: SiteService, private authService: AuthService) {}

  ngOnInit(): void {
    this.isAdmin = this.authService.isAdmin(); 
    this.loadReservations();
    this.loadParticipantReservations();
  }

  loadReservations(): void {
    if (this.isAdmin) {
      this.siteService.getAllReservations().subscribe(
        (reservations) => {
          this.userReservations = reservations;
          console.log('Admin reservations:', this.userReservations);
        },
        (error) => {
          console.error('Error fetching admin reservations:', error);
        }
      );
    } else {

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
  }

  loadParticipantReservations(): void {
    this.siteService.getJoinedReservations().subscribe(
      (reservations) => {
        this.participantReservations = reservations;
        console.log('Participant reservations:', this.participantReservations);
      },
      (error) => {
        console.error('Error fetching participant reservations:', error);
      }
    );
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


  showLeaveConfirmation(reservationId: number): void {
    this.selectedReservationId = reservationId;
    this.isLeaveConfirmationVisible = true;
  }

  hideLeaveConfirmation(): void {
    this.selectedReservationId = null;
    this.isLeaveConfirmationVisible = false;
  }

  confirmLeave(): void {
    if (this.selectedReservationId !== null) {
      this.leaveReservation(this.selectedReservationId);
      this.hideLeaveConfirmation();
    }
  }

  leaveReservation(reservationId: number): void {
    this.siteService.leaveReservation(reservationId).subscribe(
      (response) => {
        console.log('Successfully left the reservation:', response);
        this.loadParticipantReservations(); 
      },
      (error) => {
        console.error('Error leaving reservation:', error);
      }
    );
  }
  showParticipantRemoveConfirmation(reservationId: number, participantId: number): void {
    this.selectedReservationForParticipant = reservationId;
    this.selectedParticipantId = participantId;
    this.isParticipantRemoveConfirmationVisible = true;
  }

  hideParticipantRemoveConfirmation(): void {
    this.selectedParticipantId = null;
    this.selectedReservationForParticipant = null;
    this.isParticipantRemoveConfirmationVisible = false;
  }

  confirmRemoveParticipant(): void {
    if (this.selectedReservationForParticipant !== null && this.selectedParticipantId !== null) {
      this.siteService.removeParticipantFromReservation(this.selectedReservationForParticipant, this.selectedParticipantId).subscribe(
        (response) => {
          console.log('Participant removed successfully:', response);
          this.loadReservations(); 
          this.hideParticipantRemoveConfirmation();
        },
        (error) => {
          console.error('Error removing participant:', error);
        }
      );
    }
  }
}
