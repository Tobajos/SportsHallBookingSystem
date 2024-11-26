import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './Site/login/login.component';
import { RegisterComponent } from './Site/register/register.component';
import { HomeComponent } from './Site/home/home.component';
import { CommunityComponent } from './Site/community/community.component';
import { ProfileComponent } from './Site/profile/profile.component';


const routes: Routes = [
  {path:'', component:HomeComponent},
  {path:'login', component:LoginComponent},
  {path:'register', component:RegisterComponent},
  {path: 'community', component:CommunityComponent},
  {path: 'profile', component:ProfileComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
