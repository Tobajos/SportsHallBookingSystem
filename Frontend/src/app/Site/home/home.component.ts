import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  currentDate = new Date();
  year: number = this.currentDate.getFullYear();
  month: number = this.currentDate.getMonth();
  selectedDay: Date | null = null;
  timeSlots: string[] = [];
  startHour = 10;
  endHour = 19;
  daysInMonth: { date: Date; isToday: boolean }[] = [];

  monthNames: string[] = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  allReservations: {
    id:number;
    user: { id: number; firstname: string; lastname: string };
    date: string;
    start_time: string;
    end_time: string;
    max_participants: number;
    is_open: boolean;
  }[] = [];

  reservationData: {
    date: string,
    start_time: string,
    end_time: string
  } | null = null;

  constructor(private siteService: SiteService) {
    this.generateDaysInMonth();
    this.generateTimeSlots();
  }

  ngOnInit(): void {
    this.siteService.getAllReservations().subscribe((reservations) => {
      this.allReservations = reservations;
      console.log(this.allReservations);
    });
  }

  generateDaysInMonth() {
    const date = new Date(this.year, this.month, 1);
    this.daysInMonth = [];
    while (date.getMonth() === this.month) {
      this.daysInMonth.push({
        date: new Date(date),
        isToday: date.toDateString() === new Date().toDateString(),
      });
      date.setDate(date.getDate() + 1);
    }
  }

  generateTimeSlots() {
    this.timeSlots = [];
    for (let hour = this.startHour; hour < this.endHour; hour++) {
      const start = `${hour}:00`;
      const end = `${hour + 1}:00`;
      this.timeSlots.push(`${start} - ${end}`);
    }
  }

  isReserved(slot: string): boolean {
    if (!this.selectedDay) return false;

    const dateKey = formatDateToYYYY_MM_DD(this.selectedDay);
    const [startTime, endTime] = slot.split(' - ');

    return this.allReservations.some(reservation => {
      const isSameDate = reservation.date === dateKey;
      const reservationStartTime = reservation.start_time.slice(0, 5);
      const reservationEndTime = reservation.end_time.slice(0, 5);

      const overlaps =
        !(endTime <= reservationStartTime || startTime >= reservationEndTime);

      return isSameDate && overlaps;
    });
  }

  isSlotAvailable(slot: string): boolean {
    return !this.isReserved(slot);
  }

  isSlotOpen(slot: string): boolean {
    if (!this.selectedDay) return false;

    const dateKey = formatDateToYYYY_MM_DD(this.selectedDay);
    const [startTime, endTime] = slot.split(' - ');

    const reservation = this.allReservations.find(res => {
      const isSameDate = res.date === dateKey;
      const reservationStartTime = res.start_time.slice(0, 5);
      const reservationEndTime = res.end_time.slice(0, 5);

      const overlaps =
        !(endTime <= reservationStartTime || startTime >= reservationEndTime);

      return isSameDate && overlaps;
    });

    return reservation?.is_open || false;
  }

  getReservationDetails(slot: string): string | null {
    if (!this.selectedDay) return null;

    const dateKey = formatDateToYYYY_MM_DD(this.selectedDay);
    const [startTime, endTime] = slot.split(' - ');

    const reservation = this.allReservations.find(res => {
      const isSameDate = res.date === dateKey;
      const reservationStartTime = res.start_time.slice(0, 5);
      const reservationEndTime = res.end_time.slice(0, 5);

      const overlaps =
        !(endTime <= reservationStartTime || startTime >= reservationEndTime);

      return isSameDate && overlaps;
    });

    if (reservation) {
      const user = reservation.user;
      return `Reserved by: ${user.firstname} ${user.lastname}, Max participants: ${reservation.max_participants}, Open: ${reservation.is_open}`;
    }

    return null;
  }

  selectDay(day: Date) {
    this.selectedDay = day;
  }

  reserveTimeSlot(slot: string) {
    if (this.selectedDay) {
      const dateKey = formatDateToYYYY_MM_DD(this.selectedDay);
      const [startTime, endTime] = slot.split(' - ');

      this.reservationData = {
        date: dateKey,
        start_time: startTime,
        end_time: endTime
      };

      console.log("Reservation data being sent:", this.reservationData);

      this.siteService.createReservation(this.reservationData).subscribe(
        (response) => {
          console.log('Reservation created:', response);
        },
        (error) => {
          console.error('Error creating reservation:', error);
        }
      );
    }
  }

  joinOpenSlot(slot: string) {
    if (!this.selectedDay) return;
  
    const dateKey = formatDateToYYYY_MM_DD(this.selectedDay);
    const [startTime] = slot.split(' - ');
  
    const reservation = this.allReservations.find(res => 
      res.date === dateKey && res.start_time.startsWith(startTime)
    );
  
    if (reservation) {
      this.siteService.joinReservation(reservation.id).subscribe(
        response => {
          console.log('Successfully joined the reservation:', response);
          this.ngOnInit();
        },
        error => {
          console.error('Error joining the reservation:', error);
        }
      );
    }
  }
  
  prevMonth() {
    this.month--;
    if (this.month < 0) {
      this.month = 11;
      this.year--;
    }
    this.generateDaysInMonth();
  }

  nextMonth() {
    this.month++;
    if (this.month > 11) {
      this.month = 0;
      this.year++;
    }
    this.generateDaysInMonth();
  }

  closeModal() {
    this.selectedDay = null;
  }
}

function formatDateToYYYY_MM_DD(date: Date): string {
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear();

  return `${year}-${month}-${day}`;
}
