import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; 
import { FormsModule } from '@angular/forms'; 
import { RouterModule, Routes } from '@angular/router'; 
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './Site/login/login.component';
import { RegisterComponent } from './Site/register/register.component';
import { HomeComponent } from './Site/home/home.component';
import { NavbarComponent } from './Site/navbar/navbar.component';
import { AuthService } from './Services/auth.service';
import { CommunityComponent } from './Site/community/community.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    NavbarComponent,
    CommunityComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,  
    FormsModule,
    FontAwesomeModule       
  ],
  providers: [AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
