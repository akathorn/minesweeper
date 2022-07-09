import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'minesweeper';

  constructor(private router: Router) {
    // Code to redirect in github pages
    let redirect = localStorage.getItem('github_redirect');
    if(redirect) {
      let path = redirect.split("/").slice(2).join("/")
      localStorage.removeItem('github_redirect');
      this.router.navigate([path]);
    }
  }
}
