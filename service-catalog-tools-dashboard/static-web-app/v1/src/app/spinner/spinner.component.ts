import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.component.html',
  styleUrls: ['./spinner.component.scss']
})
export class SpinnerComponent implements OnInit {

  @Input() message: string = 'Loading the details....';
  @Input() enable: boolean = false;

  constructor() {
  }

  ngOnInit() {
  }

}
