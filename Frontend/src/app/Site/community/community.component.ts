import { Component, OnInit } from '@angular/core';
import { SiteService } from '../../Services/site.service';
import { AuthService } from '../../Services/auth.service';

@Component({
  selector: 'community',
  templateUrl: './community.component.html',
  styleUrl: './community.component.css'
})
export class CommunityComponent implements OnInit {
  posts: any[] = []

  constructor(private siteService: SiteService, private authService:AuthService){}

  ngOnInit(){
    this.getAllPosts();
  }

  getAllPosts(): void{

    this.siteService.getPosts().subscribe(
      (data:any)=>{
        this.posts = data;
        console.log('Data from API:', data);  

      },
      (error) => {
        console.error('Error', error.error)
      }
    )
  }
}
