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

  isIcon(tile: string) {
    return tile == "!" // || tile == "?"
  }

  getClassName(tile: string) {
    if (tile == " ") {
      tile = "blank"
    } else if (tile == "#") {
      tile = "hidden"
    }

    if (this.isIcon(tile)) {
      return "game-tile-icon game-tile-" + tile
    } else {
      return "game-tile-" + tile
    }
  }

  getTileIcon(tile: string) {
    switch(tile) {
      case "!": return "warning";
    }

    return "error"
  }



}
