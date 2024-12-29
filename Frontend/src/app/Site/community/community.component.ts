import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';
import { AuthService } from '../../Services/auth.service';
import { faTrash, faPenToSquare } from '@fortawesome/free-solid-svg-icons';

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
  currentUser: any;
  reservations: any[] = []; 
  selectedReservationId: number | null = null; 
  errorMessage: string | null = null;
  delete = faTrash;
  edit = faPenToSquare
  isPostDeleteConfirmationVisible: boolean = false;
  postToDelete: number | null = null;

  editingPostId: number | null = null; 
  editedContent: string = ''; 

  isAdmin: boolean = false;

  constructor(private siteService: SiteService, private authService: AuthService) {}

  ngOnInit() {
    this.currentUser = this.authService.getUser();
    this.getAllPosts();
    this.getReservations();
    console.log("userek",this.currentUser)
    this.isAdmin = this.authService.isAdmin(); 
  }

  addPost(): void {
    console.log("Dodawanie posta z rezerwacją ID:", this.selectedReservationId); 
    if (this.content.trim()) {
      const postData = {
        content: this.content,
        reservationId: this.selectedReservationId 
      };
  
      this.siteService.createPost(postData).subscribe(
        (newPost) => {
          console.log("Odpowiedź z serwera - nowy post:", newPost);
          newPost.comments = [];
          newPost.reservation = this.reservations.find(res => res.id === this.selectedReservationId);
          this.posts.unshift(newPost);

          this.ngOnInit();
          this.content = '';
          this.selectedReservationId = null;
        },
        (error) => {
          console.error('Błąd przy dodawaniu posta:', error);
        }
      );
    }
  }

  startEditingPost(postId: number, content: string): void {
    this.editingPostId = postId;
    this.editedContent = content;
  }
  
  cancelEditingPost(): void {
    this.editingPostId = null;
    this.editedContent = '';
  }
  
  saveEditedPost(): void {
    if (this.editingPostId !== null && this.editedContent.trim()) {
      this.siteService.updatePost(this.editingPostId, this.editedContent).subscribe(
        (updatedPost) => {
          const post = this.posts.find(p => p.id === this.editingPostId);
          if (post) {
            post.content = updatedPost.content;
          }
          this.cancelEditingPost();
          console.log('Post updated successfully:', updatedPost);
        },
        (error) => {
          console.error('Error updating post:', error);
        }
      );
    }
  }
  
  deleteComment(commentId: number): void {
    const post = this.posts.find(post => 
      post.comments.some((comment: { id: number }) => comment.id === commentId)
    );
  
    if (post) {
      post.comments = post.comments.filter((comment: { id: number }) => comment.id !== commentId);
    }
  
    this.siteService.deleteComment(commentId).subscribe(
      () => {
        console.log('Comment deleted successfully');
      },
      (error) => {
        console.error('Error deleting comment:', error);
      }
    );
  }
  
  
  
  
  
  confirmDeletePost(): void {
    if (this.postToDelete !== null) {
      this.siteService.deletePost(this.postToDelete).subscribe(
        () => {
          this.posts = this.posts.filter(post => post.id !== this.postToDelete);
          console.log('Post deleted successfully');
          this.hideDeleteConfirmation();
        },
        (error) => {
          console.error('Error deleting post:', error);
          this.hideDeleteConfirmation();
        }
      );
    }
  }

  getAllPosts(): void {
    this.siteService.getPosts().subscribe(
      (data: any) => {
        this.posts = data.sort((a: any, b: any) => new Date(b.date).getTime() - new Date(a.date).getTime());
  

        this.posts.forEach((post) => {
          this.siteService.getCommentsForPost(post.id).subscribe(
            (comments: any) => {
              post.commentsCount = comments.length; 
            },
            (error) => {
              console.error('Error fetching comments count:', error);
              post.commentsCount = 0; 
            }
          );
        });
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


  joinReservation(reservationId: number): void {
    this.siteService.joinReservation(reservationId).subscribe(
      response =>{
        this.errorMessage = null;
        this.ngOnInit();
      },
      (error) => {
        console.error('Error joining reservation:', error);
        this.errorMessage = error.error?.error || 'An unexpected error occurred.';
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
            post.commentsCount = post.comments.length; // Aktualizacja liczby komentarzy
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
          post.commentsCount = comments.length; // Aktualizacja liczby komentarzy
        }
      },
      (error) => {
        console.error('Error fetching comments:', error);
      }
    );
  }

  showConfirmation(postId: number): void {
    this.isPostDeleteConfirmationVisible = true;
    this.postToDelete = postId;
  }

  hideDeleteConfirmation(): void {
    this.isPostDeleteConfirmationVisible = false;
    this.postToDelete = null;
  }

  closeErrorMessage() {
    this.errorMessage = null;
  }
}
