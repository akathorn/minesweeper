import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GameComponent } from './game/game.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatIconModule} from '@angular/material/icon';

import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { BoardComponent } from './game/board/board.component';
import { TileComponent } from './game/board/tile/tile.component';




@NgModule({
  declarations: [
    AppComponent,
    GameComponent,
    BoardComponent,
    TileComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatIconModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
