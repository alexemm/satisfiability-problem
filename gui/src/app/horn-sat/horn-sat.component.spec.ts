import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HornSatComponent } from './horn-sat.component';

describe('HornSatComponent', () => {
  let component: HornSatComponent;
  let fixture: ComponentFixture<HornSatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HornSatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HornSatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
