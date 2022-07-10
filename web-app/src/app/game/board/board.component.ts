import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit {
  @Input() board!: any // Array<Array<string>> TODO
  @Input() newGameListener!: Subject<any>
  @Output() reveal = new EventEmitter<[number, number]>();
  @Output() mark = new EventEmitter<[number, number]>();
  rows?: Array<number>
  cols?: Array<number>

  constructor() { }

  press(row: number, col: number) {
    // this.reveal.next([row, col])
    this.mark.next([row, col])
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
