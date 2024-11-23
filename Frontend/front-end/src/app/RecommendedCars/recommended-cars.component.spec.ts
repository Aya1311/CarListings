import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecommendedCarsComponent } from './recommended-cars.component';

describe('RecommendedCarsComponent', () => {
  let component: RecommendedCarsComponent;
  let fixture: ComponentFixture<RecommendedCarsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecommendedCarsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RecommendedCarsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
