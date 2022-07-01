import { Component, OnInit } from '@angular/core';
declare var loadPyodide: any

@Component({
  selector: 'app-python',
  templateUrl: './python.component.html',
  styleUrls: ['./python.component.scss']
})
export class PythonComponent implements OnInit {
  pyodide: any = null
  state: number = 0
  code_url: string = "assets/game.tar.gz"
  game?: any = null
  rows?: Array<number>
  cols?: Array<number>

  constructor() {
    loadPyodide().then((pyodide: any) => this.initPyodide(pyodide))
  }

  ngOnInit(): void {
  }

  initPyodide(pyodide: any): void {
    this.pyodide = pyodide
    console.log(pyodide.runPython(`
      import sys
      sys.version
    `))

    this.loadModules().then((_) => {
      this.game = pyodide.runPython(`
        import game
        game.Game()
      `)
      this.rows = Array(this.game.rows).fill(0).map((x,i)=>i);
      this.cols = Array(this.game.cols).fill(0).map((x,i)=>i);
      // console.log(this.game.board)
      // console.log(this.game.board.get(0).get(1))
    })
  }

  async loadModules(): Promise<any> {
    let response = await fetch(this.code_url)
    let buffer = await response.arrayBuffer()
    await this.pyodide.unpackArchive(buffer, "tar.gz")

    this.pyodide.runPython(`
      import os
      print("Modules loaded:", os.listdir())
    `)


    return this.pyodide.pyimport("game");
  }

}
