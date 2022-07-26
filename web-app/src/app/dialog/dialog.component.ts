import { Component, EventEmitter, Inject, OnInit, Output } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

export interface EndDialogData {
  victory: boolean;
}

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.scss']
})
export class DialogComponent implements OnInit {

  constructor(public dialog: MatDialog) {}

  @Output() newGame = new EventEmitter();

  openHelp() {
    const dialogRef = this.dialog.open(DialogHelp);
  }

  openGameEnd(victory: boolean) {
    const dialogRef = this.dialog.open(DialogEnd,
      {
        data: { victory: victory }
      });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.newGame.next(null)
      }
    });
  }

  ngOnInit(): void {
    // this.openHelp()
  }

}


@Component({
  selector: 'dialog-end',
  templateUrl: 'dialog-end.html',
})
export class DialogEnd {
  constructor(@Inject(MAT_DIALOG_DATA) public data: EndDialogData) {}
}

@Component({
  selector: 'dialog-help',
  templateUrl: 'dialog-help.html',
})
export class DialogHelp {
  constructor(public dialogRef: MatDialogRef<DialogHelp>) {}
}