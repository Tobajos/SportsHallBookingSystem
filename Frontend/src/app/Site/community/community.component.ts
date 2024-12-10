import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';
import { AuthService } from '../../Services/auth.service';

@Component({
  selector: 'community',
  templateUrl: './community.component.html',
  styleUrls: ['./community.component.css']
})
export class CommunityComponent implements OnInit {
  posts: any[] = [];
  content: string = "";
  commentContent: string = ''; 
  activeCommentPostId: number | null = null; 

  reservations: any[] = []; 
  selectedReservationId: number | null = null; 

  constructor(private siteService: SiteService, private authService: AuthService) {}

  ngOnInit() {
    this.getAllPosts();
    this.getReservations();
  }

  addPost(): void {
    if (this.content.trim()) {
      const postData = {
        content: this.content,
        reservationId: this.selectedReservationId // Dodajemy wybraną rezerwację
      };
  
      this.siteService.createPost(postData).subscribe(
        (newPost) => {
          newPost.comments = [];
          newPost.reservation = this.reservations.find(res => res.id === this.selectedReservationId); // Przypisujemy rezerwację do posta
          this.posts.unshift(newPost);
          this.content = '';
          this.selectedReservationId = null; // Resetujemy wybraną rezerwację po dodaniu posta
        },
        (error) => {
          console.error('Error adding post:', error);
        }
      );
    }
  }

  getAllPosts(): void {
    this.siteService.getPosts().subscribe(
      (data: any) => {
        this.posts = data.sort((a: any, b: any) => new Date(b.date).getTime() - new Date(a.date).getTime());
        console.log('Data from API (sorted):', this.posts);
      },
      (error) => {
        console.error('Error fetching posts:', error);
      }
    );
  }
  
  getReservations(): void {
    this.siteService.getUserReservations().subscribe(
      (data: any) => {
        this.reservations = data;
        console.log("rezerwacje na tablicy",this.reservations)
      },
      (error) => {
        console.error('Error fetching reservations:', error);
      }
    );
  }

  // Dołączenie do rezerwacji
  joinReservation(reservationId: number): void {
    this.siteService.joinReservation(reservationId).subscribe(
      (updatedReservation) => {
        // Opcjonalnie: Po dołączeniu do rezerwacji, zaktualizuj liczbę uczestników
        const reservation = this.reservations.find(r => r.id === reservationId);
        if (reservation) {
          reservation.currentParticipants += 1; // Zwiększ liczbę uczestników
        }
      },
      (error) => {
        console.error('Error joining reservation:', error);
      }
    );
  }

  toggleCommentInput(postId: number): void {
    if (this.activeCommentPostId === postId) {
      this.activeCommentPostId = null;
      this.commentContent = '';
    } else {
      this.activeCommentPostId = postId;
      this.commentContent = '';

      const post = this.posts.find(p => p.id === postId);
      if (post && !post.comments) {
        this.getCommentsForPost(postId);
      }
    }
  }

  addComment(postId: number): void {
    if (this.commentContent.trim()) {
      this.siteService.createComment(postId, this.commentContent).subscribe(
        (newComment) => {
          const post = this.posts.find(p => p.id === postId);
          if (post) {
            post.comments = post.comments || [];
            post.comments.push(newComment); 
            post.comments.sort((a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime());
            this.commentContent = ''; 
          }
        },
        (error) => {
          console.error('Error adding comment:', error);
        }
      );
    }
  }

  getCommentsForPost(postId: number): void {
    this.siteService.getCommentsForPost(postId).subscribe(
      (comments: any) => {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
          post.comments = comments.sort((a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime());
        }
      },
      (error) => {
        console.error('Error fetching comments:', error);
      }
    );
  }
}
