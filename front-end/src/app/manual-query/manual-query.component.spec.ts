import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManualQueryComponent } from './manual-query.component';

describe('ManualQueryComponent', () => {
  let component: ManualQueryComponent;
  let fixture: ComponentFixture<ManualQueryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManualQueryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManualQueryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
