import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CommonModule } from '@angular/common';
import { CreateArtistComponent } from './create-artist/create-artist.component';
import { DialogComponent } from "../shared/dialog/dialog.component";
import { AllArtistsComponent } from './all-artists/all-artists.component';
import { ArtistCardComponent } from './all-artists/artist-card/artist-card.component';

@NgModule({
    declarations: [
        CreateArtistComponent,
        AllArtistsComponent,
        ArtistCardComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        DialogComponent,
    ],
    exports:[
        AllArtistsComponent
    ]
})
export class ArtistsModule {}
