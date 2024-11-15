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

  constructor(private siteService: SiteService, private authService: AuthService) {}

  ngOnInit() {
    this.getAllPosts();
  }

  addPost(): void {
    if (this.content.trim()) {
      this.siteService.createPost(this.content).subscribe(
        (newPost) => {
          newPost.comments = [];
          this.posts.unshift(newPost);
          this.content = '';  
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
        this.posts = data;
        console.log('Data from API:', data);
      },
      (error) => {
        console.error('Error fetching posts:', error);
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
            post.comments.unshift(newComment); 
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
          post.comments = comments; 
        }
      },
      (error) => {
        console.error('Error fetching comments:', error);
      }
    );
  }
}
