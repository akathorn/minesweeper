import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-tile',
  templateUrl: './tile.component.html',
  styleUrls: ['./tile.component.scss']
})
export class TileComponent implements OnInit {
  @Input() tile!: string

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
