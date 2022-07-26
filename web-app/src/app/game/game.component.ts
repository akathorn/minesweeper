import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { Subject } from 'rxjs';
import { DialogComponent } from '../dialog/dialog.component';
import { PythonService } from '../python.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit, AfterViewInit {
  private game_module?: any = null
  game?: any = null
  newGameListener: Subject<any> = new Subject()

  @ViewChild(DialogComponent) dialog!: DialogComponent

  constructor(
    private pythonService: PythonService
  ) {
    pythonService.getGame().then(
        module => {
          this.game_module = module
          this.newGame(16, 16, 40)
        }
    )
  }

  newGame(rows: number, cols: number, n_mines: number) {
    console.log("Initializing game")
    this.game = this.game_module.Game(
      rows,
      cols,
      n_mines,
      true,
      null,
      (victory: boolean) => this.gameEnd(victory))
    this.newGameListener.next(this.game)
  }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.dialog.openHelp()
  }

  reveal(pos: [number, number]) {
    // this.game.mark(pos[0], pos[1])
    this.game.reveal(pos[0], pos[1])
  }

  mark(pos: [number, number]) {
    this.game.mark(pos[0], pos[1])
  }

  gameEnd(victory: boolean) {
    this.dialog.openGameEnd(victory)
  }

}
