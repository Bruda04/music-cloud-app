import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { CreateArtistComponent } from './create-artist/create-artist.component';
import { DialogComponent } from "../shared/dialog/dialog.component";
import { ArtistCardComponent } from './all-artists/artist-card/artist-card.component';

@NgModule({
    declarations: [
        CreateArtistComponent,
        ArtistCardComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        DialogComponent,
    ],
    exports:[
        ArtistCardComponent
    ]
})
export class ArtistsModule {}
