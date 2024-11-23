// saved-cars.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CarService } from '../services';

@Component({
  selector: 'app-saved-cars',
  templateUrl: './saved-cars.component.html',
  styleUrls: ['./saved-cars.component.css']
})
export class SavedCarsComponent implements OnInit {
  savedCars: any[] = [];
  userId!: number;

  constructor(private carService: CarService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.userId = +params['id'];
      this.loadSavedCars();
    });
  }

  loadSavedCars(): void {
    this.carService.getSavedCars(this.userId).subscribe(data => {
      this.savedCars = data;
    });
  }
}
