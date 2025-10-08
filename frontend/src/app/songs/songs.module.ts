import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { DialogComponent } from "../shared/dialog/dialog.component";
import { CreateSongComponent } from './create-song/create-song.component';

@NgModule({
    declarations: [
        CreateSongComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        DialogComponent,
    ],
    exports:[
        
    ]
})
export class SongsModule {}
