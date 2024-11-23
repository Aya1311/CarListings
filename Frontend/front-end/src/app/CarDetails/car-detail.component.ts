// car-detail.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CarService } from '../services';

@Component({
  selector: 'app-car-detail',
  templateUrl: './car-detail.component.html',
  styleUrls: ['./car-detail.component.css']
})
export class CarDetailComponent implements OnInit {
  car: any;
  userId!: number;


  constructor(private route: ActivatedRoute, private carService: CarService) {}

  ngOnInit(): void {
    const carId = this.route.snapshot.paramMap.get('id');
    if (carId) {
      this.carService.getCars().subscribe(data => {
        const allCars = [...data.avito_cars];
        this.car = allCars.find(c => c.id_car === +carId);
      });
    } else {
      console.error('Car ID is null or undefined');
    }
  }
  
}
