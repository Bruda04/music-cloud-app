import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { CreateArtistComponent } from './create-artist/create-artist.component';
import { DialogComponent } from "../shared/dialog/dialog.component";

@NgModule({
    declarations: [
        CreateArtistComponent
    ],
    imports: [
    BrowserModule,
    FormsModule,
    CommonModule,
    DialogComponent
],
})
export class ArtistsModule {}
