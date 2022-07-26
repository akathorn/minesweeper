import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  @Input() game!: any
  @Output() newGame = new EventEmitter();
  @Output() hint = new EventEmitter();
  @Output() help = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

}
