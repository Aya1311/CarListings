import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SavedCarsComponent } from './saved-cars.component';

describe('SavedCarsComponent', () => {
  let component: SavedCarsComponent;
  let fixture: ComponentFixture<SavedCarsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SavedCarsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SavedCarsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
