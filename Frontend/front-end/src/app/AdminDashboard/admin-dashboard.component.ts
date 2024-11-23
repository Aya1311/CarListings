import { Component, OnInit } from '@angular/core';
import { AdminService } from '../services';
import { ClientService } from '../services';
import { CarService } from '../services'; 
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {

  admins: any[] = [];
  filteredAdmins: any[] = [];
  clients: any[] = [];
  filteredClients: any[] = [];
  totalClients: number = 0;
  totalAds: number = 0;

  constructor(
    private adminService: AdminService,
    private clientService: ClientService,
    private carService: CarService // Ajoutez CarService ici
  ) { }

  ngOnInit(): void {
    this.loadAdmins();
    this.loadClients();
    this.loadTotalAds();
    this.loadTotalClients();

  }

  loadTotalClients(): void {
    this.clientService.getClientCount().subscribe(data => {
      this.totalClients = data.count;
      document.getElementById('total-clients')!.innerText = this.totalClients.toString();
    });
  }

  loadAdmins(): void {
    this.adminService.getAdmins().subscribe(data => {
      console.log(data); 
      this.admins = data;
      this.filteredAdmins = data; 
    });
  }
  loadClients(): void {
    this.clientService.getClients().subscribe(data => {
      console.log(data);
      this.clients = data.map(client => ({
        id: client.user.id,
        username: client.user.username,
        email: client.user.email,
        age: client.age,
        budget_min: client.budget_min,
        budget_max: client.budget_max,
        boite_preferee: client.boite_preferee,
        carburant_prefere: client.carburant_prefere
      }));
      this.filteredClients = this.clients;
    });
  }
  loadTotalAds(): void {
    this.carService.getCarsCount().subscribe(data => {
      this.totalAds = data.count; 
      document.getElementById('total-ads')!.innerText = this.totalAds.toString();
    });
  }

  createAdmin(): void {
    const username = prompt("Entrez le nom d'utilisateur de l'administrateur");
    const email = prompt("Entrez l'email de l'administrateur");
    const password = prompt("Entrez le mot de passe de l'administrateur");

    if (username && email && password) {
      this.adminService.createAdmin(username, email, password).subscribe(response => {
        if (response.user) { 
          alert('Administrateur créé avec succès');
          this.loadAdmins(); 
        } else {
          alert('Erreur lors de la création de l\'administrateur');
        }
      });
    }
  }

  filterAdmins(event: Event): void {
    const input = event.target as HTMLInputElement; 
    const searchTerm = input.value;
    this.filteredAdmins = this.admins.filter(admin =>
      admin.user.username.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  downloadCSV(data: any[], filename: string): void {
    const replacer = (key: any, value: any) => value === null ? '' : value;
    const header = Object.keys(data[0]);
    const csv = [
      header.join(','), 
      ...data.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
    ].join('\r\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    saveAs(blob, `${filename}.csv`);
  }

  downloadAdminsCSV(): void {
    this.downloadCSV(this.filteredAdmins, 'admins');
  }

  downloadClientsCSV(): void {
    this.downloadCSV(this.filteredClients, 'clients');
  }
}
