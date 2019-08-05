import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ShowPipelinesComponent} from './show-pipelines.component';

describe('ShowPipelinesComponent', () => {
  let component: ShowPipelinesComponent;
  let fixture: ComponentFixture<ShowPipelinesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ShowPipelinesComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowPipelinesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
