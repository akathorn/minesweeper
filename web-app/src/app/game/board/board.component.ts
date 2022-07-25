import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit {
  doubleClickThreshold = 250;
  private lastClick: number = 0

  board!: any // Array<Array<string>> TODO
  @Input() newGameListener!: Subject<any>
  
  @Output() reveal = new EventEmitter<[number, number]>();
  @Output() mark = new EventEmitter<[number, number]>();
  
  rows?: Array<number>
  cols?: Array<number>

  constructor() {
  }

  doubleClick(row: number, col: number) {
    this.reveal.next([row, col])
  }

  singleClick(row: number, col: number) {
    this.mark.next([row, col])
  }

  click(row: number, col: number) {
    if (Date.now() - this.lastClick < this.doubleClickThreshold) {
      this.doubleClick(row, col)
      this.lastClick = 0
    } else {
      this.singleClick(row, col)
      this.lastClick = Date.now()
    }
  }

  ngOnInit(): void {
    this.newGameListener.subscribe((game) => this.newGame(game))
  }

  getTile(row: number, col: number) {
    return () => this.board.get(row).get(col)
  }

  newGame(game: any) {
    this.board = game.board.tiles
    this.rows = Array(game.board.rows).fill(0).map((x,i)=>i);
    this.cols = Array(game.board.cols).fill(0).map((x,i)=>i);
  }
}
