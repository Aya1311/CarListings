//client-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CarService } from '../services'; 

@Component({
  selector: 'app-client-dashboard',
  templateUrl: './client-dashboard.component.html',
  styleUrls: ['./client-dashboard.component.css']
})
export class ClientDashboardComponent implements OnInit {
  cars: any[] = [];
  filteredCars: any[] = [];
  filters = {
    title: '',
    carburant: '',
    boite: '',
    nombreDePortes: '',
    ville: '',
    year: null,
    minPrice: null as number | null,
    maxPrice: null as number | null
  };
  displayedCars: any[] = [];
  loadMoreCount = 30;
  userId!: number;
  selectedCars: any[] = []; 

  constructor(
    private carService: CarService, 
    private route: ActivatedRoute, 
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.userId = +params['id'];
      this.loadCars();
    });
  }

  loadCars(): void {
    this.carService.getCars().subscribe(data => {
      this.cars = [...data.avito_cars];
      this.cars = this.sortByIdDescending(this.cars); 
      this.filteredCars = [...this.cars];
      this.displayedCars = this.filteredCars.slice(0, this.loadMoreCount);
    });
  }

  sortByIdDescending(array: any[]): any[] {
    return array.sort((a, b) => b.id_car - a.id_car);
  }
  convertPrice(priceStr: string): number | null {
    if (priceStr === 'N/A' || priceStr === 'Prix non spécifié') {
      return null; 
    }
  
    const priceNumber = parseFloat(priceStr.replace(/[^\d,]/g, '').replace(',', '.'));
  
    return isNaN(priceNumber) ? null : priceNumber;
  }

  loadMore(): void {
    const nextCount = this.displayedCars.length + this.loadMoreCount;
    this.displayedCars = this.filteredCars.slice(0, nextCount);
  }
 
  applyFilters(): void {
    this.filteredCars = this.cars.filter(car => {
      const carPrice = this.convertPrice(car.price);
      const carYear = parseInt(car.year, 10); 
  
      return (!this.filters.title || car.title.toLowerCase().includes(this.filters.title.toLowerCase())) &&
             (!this.filters.carburant || car.carburant === this.filters.carburant) &&
             (!this.filters.boite || car.boite === this.filters.boite) &&
             (!this.filters.ville || car.ville.toLowerCase().includes(this.filters.ville.toLowerCase())) &&
             (!this.filters.year || carYear === parseInt(this.filters.year, 10)) && // Comparer les années en tant que nombres
             (carPrice !== null) &&
             (this.filters.minPrice === null || carPrice >= this.filters.minPrice) &&
             (this.filters.maxPrice === null || carPrice <= this.filters.maxPrice);
    });
  
    this.displayedCars = this.filteredCars.slice(0, this.loadMoreCount);
  }
  
  
  
  onCarSelectionChange(car: any, event: any): void {
    if (event.target.checked) {
      if (this.selectedCars.length < 2) {
        this.selectedCars.push(car);
      } else {
        event.target.checked = false; 
      }
    } else {
      this.selectedCars = this.selectedCars.filter(selectedCar => selectedCar.id_car !== car.id_car);
    }
  }

  compareSelectedCars(): void {
    if (this.selectedCars.length === 2) {
      const car1Id = this.selectedCars[0].id_car;
      const car2Id = this.selectedCars[1].id_car;
      this.router.navigate(['/compare', car1Id, car2Id]);
    } else {
      alert('Veuillez choisir exactement 2 voitures.');
    }
  }

  saveCar(car: any): void {
    this.carService.recordSave(this.userId, car.id_car).subscribe(
      () => {
        alert('Voiture sauvegardée avec succès.');
      },
      error => {
        console.error('Erreur lors de la sauvegarde de la voiture:', error);
      }
    );
  }

  navigateTo(page: string): void {
    if (page === 'site-suggestions') {
      this.router.navigate([`/recommended-cars/${this.userId}`]);
    } else {
      this.router.navigate([`/${page}`, this.userId]);
    }
  }
  
  logout(): void {
    this.router.navigate(['/login']);
  }

  viewCarDetail(carId: number): void {
    const car = this.filteredCars.find(c => c.id_car === carId);

    if (car) {
      this.carService.recordVisit(this.userId, carId).subscribe(
        () => {
          this.router.navigate(['/car-detail', carId]);
        },
        error => {
          console.error('Erreur lors de l\'enregistrement de la visite:', error);
        }
      );
    } else {
      console.error('Voiture non trouvée avec ID:', carId);
    }
  }
}
