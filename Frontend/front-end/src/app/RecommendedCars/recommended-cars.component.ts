// recommended-cars.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CarService } from '../services'; 

@Component({
  selector: 'app-recommended-cars',
  templateUrl: './recommended-cars.component.html',
  styleUrls: ['./recommended-cars.component.css']
})
export class RecommendedCarsComponent implements OnInit {
  cars: any[] = [];
  displayedCars: any[] = [];
  userId!: number;
  itemsPerPage: number = 30;
  currentPage: number = 1;

  constructor(
    private carService: CarService, 
    private route: ActivatedRoute, 
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.userId = +params['id'];
      this.loadRecommendedCars();
    });
  }

  loadRecommendedCars(): void {
    this.carService.getRecommendedCars(this.userId).subscribe(data => {
      this.cars = data;  // Assurez-vous que `data` contient directement les voitures recommandées
      this.updateDisplayedCars();
    });
  }

  updateDisplayedCars(): void {
    this.displayedCars = this.cars.slice(0, this.currentPage * this.itemsPerPage);
  }

  loadMore(): void {
    this.currentPage++;
    this.updateDisplayedCars();
  }

  viewCarDetail(carId: number): void {
    this.router.navigate(['/car-detail', carId]);
  }
}
