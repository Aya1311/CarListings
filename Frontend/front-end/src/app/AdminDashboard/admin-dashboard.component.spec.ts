// admin-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { AdminService } from '../services';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  admins: any[] = [];
  filteredAdmins: any[] = [];
  
  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.fetchAdmins();
  }

  fetchAdmins(): void {
    this.adminService.getAdmins().subscribe(data => {
      this.admins = data;
      this.filteredAdmins = data;
    });
  }

  onSearch(event: any): void {
    const searchValue = event.target.value.toLowerCase();
    this.filteredAdmins = this.admins.filter(admin =>
      admin.user.username.toLowerCase().includes(searchValue)
    );
  }

  createAdmin(): void {
    const username = prompt('Enter username:');
    const email = prompt('Enter email:');
    const password = prompt('Enter password:');
    
    if (username && email && password) {
      this.adminService.createAdmin(username, email, password)
        .subscribe(() => {
          this.fetchAdmins();
        });
    }
  }
}
