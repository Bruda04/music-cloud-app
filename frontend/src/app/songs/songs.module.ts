import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { DialogComponent } from "../shared/dialog/dialog.component";
import { CreateSongComponent } from './create-song/create-song.component';
import { SongCardComponent } from './all-songs/song-card/song-card.component';

@NgModule({
    declarations: [
        CreateSongComponent,
        SongCardComponent,
    ],
    imports: [
        CommonModule,
        FormsModule,
        DialogComponent,
    ],
    exports:[
        SongCardComponent
    ]
})
export class SongsModule {}
