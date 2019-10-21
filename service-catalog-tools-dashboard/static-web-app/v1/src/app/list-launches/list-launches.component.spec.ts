import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ListLaunchesComponent} from './list-launches.component';

describe('ListLaunchesComponent', () => {
  let component: ListLaunchesComponent;
  let fixture: ComponentFixture<ListLaunchesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ListLaunchesComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ListLaunchesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
