import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
declare var loadPyodide: any

@Injectable({
  providedIn: 'root'
})
export class PythonService {
  private pyodide: any = null
  private wait_for_pyodide: Subject<any> = new Subject()
  code_url: string = "assets/game.tar.gz"

  constructor() {
  }

  async initPyodide(pyodide: any) {
    this.pyodide = pyodide
    this.wait_for_pyodide.next(null)

    console.log(pyodide.runPython(`
      import sys
      sys.version
    `))
  }

  async loadModules() {
    if (!this.pyodide) {
      this.initPyodide(await loadPyodide())
    }

    let response = await fetch(this.code_url)
    let buffer = await response.arrayBuffer()
    console.log(buffer)
    await this.pyodide.unpackArchive(buffer, "tar.gz")

    this.pyodide.runPython(`
      import os
      print("Modules loaded:", os.listdir())
    `)
  }

  async getGame() {
    await this.loadModules()
    return this.pyodide.runPython(`
      import game
      game.Game()
    `)
  }

}
