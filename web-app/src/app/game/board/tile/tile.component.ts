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
    return tile == "!" || tile == "?" || tile == "X" || tile == "O"
  }

  getClassName(tile: string) {
    let r = (this.isIcon(tile) ? "game-tile-icon " : "") + "game-tile-"

    switch(tile) {
      case "#": return r + "unrevealed";
      case " ": return r + "blank";
      case "!": return r + "mark1";
      case "?": return r + "mark2";
      case "X": return r + "mine";
      case "O": return r + "hint";
      default: return r + tile;
    }
  }

  getTileIcon(tile: string) {
    switch(tile) {
      case "!": return "dangerous";
      case "?": return "not_listed_location";
      case "X": return "heart_broken";
      case "O": return "star";
    }

    return "error"
  }



}
