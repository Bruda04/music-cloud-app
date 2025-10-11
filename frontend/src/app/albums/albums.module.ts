import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { DialogComponent } from "../shared/dialog/dialog.component";
import { CreateAlbumComponent } from './create-album/create-album.component';
import { AlbumCardComponent } from './all-albums/album-card/album-card.component';
import { RouterModule } from '@angular/router';
import { AlbumDetailsComponent } from './details/details.component';

@NgModule({
    declarations: [
        CreateAlbumComponent,
        AlbumCardComponent,
        AlbumDetailsComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        DialogComponent,
        RouterModule
    ],
    exports:[
        AlbumCardComponent
    ]
})
export class AlbumsModule {}
