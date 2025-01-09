import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';
import { AuthService } from '../../Services/auth.service';
import { faTrash, faBars, faRightFromBracket, faUserXmark } from '@fortawesome/free-solid-svg-icons';
import { jsPDF } from 'jspdf';




@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {


  kick = faUserXmark;
  leave = faRightFromBracket;
  edit = faBars;
  delete = faTrash;


  userReservations: any[] = [];
  participantReservations: any[] = [];
  selectedReservationId: number | null = null;
  editingReservationId: number | null = null;
  editingData: any = {};
  isAdmin: boolean = false;


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

  generatePDF(): void {
    const doc = new jsPDF();
  

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(18);
    doc.text('Reservations Report', 105, 20, { align: 'center' });
  

    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    doc.text(`Report generated by: ${this.authService.getUser().firstname} ${this.authService.getUser().lastname}`, 105, 30, { align: 'center' });
    doc.text(`Date: ${new Date().toLocaleDateString()} Time: ${new Date().toLocaleTimeString()}`, 105, 38, { align: 'center' });
  

    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    const reservationsThisMonth = this.userReservations.filter(reservation => {
      const reservationDate = new Date(reservation.date);
      return reservationDate.getMonth() === currentMonth && reservationDate.getFullYear() === currentYear;
    });
    const totalReservationsThisMonth = reservationsThisMonth.length;
  
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(14);
    doc.text(`Total Reservations This Month: ${totalReservationsThisMonth}`, 10, 50);
  

    doc.setLineWidth(0.5);
    doc.line(10, 55, 200, 55);
  

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(12);
    let y = 65;
  
    this.userReservations.forEach((reservation, index) => {
      if (y > 270) { 
        doc.addPage();
        y = 20;
      }
  

      doc.setFont('helvetica', 'bold');
      doc.text(`Reservation ${index + 1}`, 10, y);
      y += 10;

      doc.setFont('helvetica', 'normal');
      doc.text(`Date: ${reservation.date}`, 10, y);
      y += 8;
      doc.text(`Start Time: ${reservation.start_time}`, 10, y);
      y += 8;
      doc.text(`End Time: ${reservation.end_time}`, 10, y);
      y += 8;
      doc.text(`Max Participants: ${reservation.max_participants}`, 10, y);
      y += 8;
      doc.text(`Open Reservation: ${reservation.is_open ? 'Yes' : 'No'}`, 10, y);
      y += 10;
  
      if (reservation.participants?.length > 0) {
        doc.text('Participants:', 10, y);
        y += 8;
        reservation.participants.forEach((participant: any, participantIndex: number) => {
          doc.text(`  ${participantIndex + 1}. ${participant.firstname} ${participant.lastname}`, 15, y);
          y += 8;
        });
      } else {
        doc.text('Participants: None', 10, y);
        y += 10;
      }
  
      doc.setLineWidth(0.2);
      doc.line(10, y, 200, y);
      y += 10;
    });

    doc.save('Reservations_Report.pdf');
  }
  
}