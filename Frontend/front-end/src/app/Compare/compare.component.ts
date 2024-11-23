//compare.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CarService } from '../services';

@Component({
  selector: 'app-compare',
  templateUrl: './compare.component.html',
  styleUrls: ['./compare.component.css']
})
export class CompareComponent implements OnInit {
  car1: any;
  car2: any;

  constructor(private route: ActivatedRoute, private carService: CarService) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const car1Id = +params['car1Id'];
      const car2Id = +params['car2Id'];
      this.loadCarDetails(car1Id, car2Id);
    });
  }

  loadCarDetails(car1Id: number, car2Id: number): void {
    this.carService.getCarDetails(car1Id).subscribe(car1 => {
      this.car1 = car1;
      this.carService.getCarDetails(car2Id).subscribe(car2 => {
        this.car2 = car2;
      });
    });
  }
}



