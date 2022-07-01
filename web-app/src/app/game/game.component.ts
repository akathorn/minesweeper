import { Component, OnInit } from '@angular/core';
import { PythonService } from '../python.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {
  game?: any = null
  rows?: Array<number>
  cols?: Array<number>

  constructor(
    private pythonService: PythonService
  ) {
    pythonService.getGame().then(
        game => this.initGame(game)
    )
  }

  initGame(game: any) {
    console.log("Initializing game")
    this.game = game
    this.rows = Array(this.game.rows).fill(0).map((x,i)=>i);
    this.cols = Array(this.game.cols).fill(0).map((x,i)=>i);
  }

  ngOnInit(): void {
  }

  reveal(row: number, col: number) {
    this.game.reveal(row, col)
  }

  getClassName(row: number, col: number) {
    let tile = this.game.board.get(row).get(col)
    if (tile == " ") {
      tile = "blank"
    } else if (tile == "#") {{
      tile = "hidden"
    }}
    return 'game-tile-' + tile
  }

  getTile(row: number, col: number) {
    let tile = this.game.board.get(row).get(col)
    if (tile == " ") {
      tile = "_"
    } else if (tile == "#") {{
      tile = "-"
    }}

    return tile
  }

}
