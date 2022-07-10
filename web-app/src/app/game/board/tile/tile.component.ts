import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Observable, Subject } from 'rxjs';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['./tile.component.scss']
})
export class TileComponent implements OnInit {
  @Input() tile!: string
  // @Input() pos!: [number, number]
  // @Input() board!: any // Array<Array<string>> TODO
  @Output() press = new EventEmitter();
  // tileCharacter: Observable<string>

  constructor() { }

  ngOnInit(): void {
  }

  getTileChar(tile: string) {
    if (tile == " ") {
      tile = "_"
    } else if (tile == "#") {
      tile = "-"
    }
    return tile
  }

  getClassName(tile: string) {
    if (tile == " ") {
      tile = "blank"
    } else if (tile == "#") {
      tile = "hidden"
    }
    return 'game-tile-' + tile
  }

}
