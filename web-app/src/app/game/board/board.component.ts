import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit {
  threshold = 200;
  private lastPress: number = 0

  @Input() board!: any // Array<Array<string>> TODO
  @Input() newGameListener!: Subject<any>
  
  @Output() reveal = new EventEmitter<[number, number]>();
  @Output() mark = new EventEmitter<[number, number]>();
  
  rows?: Array<number>
  cols?: Array<number>

  constructor() {
  }

  press() {
    this.lastPress = Date.now()
  }

  longPress(row: number, col: number) {
    this.reveal.next([row, col])
  }

  shortPress(row: number, col: number) {
    this.mark.next([row, col])
  }

  click(row: number, col: number) {
    if (Date.now() - this.lastPress > this.threshold) {
      this.longPress(row, col)
    } else {
      this.shortPress(row, col)
    }
  }

  ngOnInit(): void {
    this.newGameListener.subscribe((game) => this.newGame(game))
  }

  getTile(row: number, col: number) {
    return () => this.board.get(row).get(col)
  }

  newGame(game: any) {
    this.board = game.board
    this.rows = Array(game.rows).fill(0).map((x,i)=>i);
    this.cols = Array(game.cols).fill(0).map((x,i)=>i);
  }
}
