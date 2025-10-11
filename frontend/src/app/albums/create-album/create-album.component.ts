import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Album, AlbumTrack, TrackDTO } from '../model/album.model';
import { ArtistService } from '../../artists/service/artist.service';
import { Artist } from '../../artists/model/artist.model';
import { AlbumService } from '../service/album.service';
import { DialogType } from '../../shared/dialog/dialog.component';
import { Genre } from '../../songs/model/genre.model';
import { GenreService } from '../../songs/service/genre.service';

@Component({
  selector: 'app-create-album',
  templateUrl: './create-album.component.html',
  styleUrls: ['../../shared/themes/forms.css'],
  standalone: false
})
export class CreateAlbumComponent implements OnInit {
    album: Album = {
        title: '',
        artistIds: [],
        genres: [],
        tracks: [],
        other: {}
    };

    tracks: AlbumTrack[] = [{ title: '', file: undefined, dragging: false }];
    fileInputMap = new Map<AlbumTrack, HTMLInputElement>();

    artists: Artist[] = [];
    genres: Genre[] = [];

    genreInput = '';
    genreInputManual = '';
    artistInput = '';
    otherKey = '';
    otherValue = '';

    loading = false;
    errorMessage = '';
    dialogType: DialogType = 'message';
    dialogTitle = '';
    dialogMessage = '';
    showDialog = false;

    constructor( private artistService: ArtistService, private genreService: GenreService, private albumService: AlbumService, private router: Router) {}

    ngOnInit() {
        this.artists = this.artistService.getAllMock();
        this.genres = this.genreService.getAllMock();
    }

    addGenre() {
        const value = this.genreInput.trim() || this.genreInputManual.trim();
        if (value && !this.album.genres.includes(value)) {
        this.album.genres.push(value);
        this.genreInput = '';
        this.genreInputManual = '';
        }
    }

    removeGenre(index: number) {
        this.album.genres.splice(index, 1);
    }

    addArtist() {
        if (this.artistInput.trim() && !this.album.artistIds.includes(this.artistInput)) {
        this.album.artistIds.push(this.artistInput.trim());
        this.artistInput = '';
        }
    }

    removeArtist(index: number) {
        this.album.artistIds.splice(index, 1);
    }

    addOther() {
        if (this.otherKey.trim()) {
        this.album.other![this.otherKey.trim()] = this.otherValue;
        this.otherKey = '';
        this.otherValue = '';
        }
    }

    removeOther(key: string) {
        delete this.album.other![key];
    }

    addTrack() {
        this.tracks.push({ title: '', file: undefined });
    }

    removeTrack(index: number) {
        this.tracks.splice(index, 1);
    }

    onFileSelected(event: any, track: AlbumTrack) {
    const file = event.target.files[0];
    if (file) {
        track.file = file;
    }
    }

    onFileDropped(event: DragEvent, track: AlbumTrack) {
    event.preventDefault();
    track.dragging = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        track.file = event.dataTransfer.files[0];
    }
    }

    onDragOver(event: DragEvent, track: AlbumTrack) {
    event.preventDefault();
    track.dragging = true;
    }

    onDragLeave(event: DragEvent, track: AlbumTrack) {
    event.preventDefault();
    track.dragging = false;
    }

    async submit() {

    if (!this.album.title.trim() || this.album.artistIds.length === 0 || this.album.genres.length === 0) {
        this.showError('Title and at least one Artist and Genre are required');
        return;
    }

    for (let t of this.tracks) {
        if (!t.title.trim() || !t.file) {
        this.showError('Each track must have a title and an audio file');
        return;
        }
    }

    this.loading = true;

    try {
        const tracksPayload:TrackDTO[] = await Promise.all(
            this.tracks.map(async (t) => ({
                title: t.title.trim(),
                fileKey: await this.convertFileToBase64(t.file!)
            }))
        );

        const payload:Album = {
            title: this.album.title,
            artistIds: this.album.artistIds,
            genres: this.album.genres,
            tracks: tracksPayload,
            other: this.album.other
        };

        this.albumService.create(payload).subscribe({
        next: (res) => {
            this.loading = false;
            this.showMessage(res.message);
        },
        error: (err) => {
            console.error(err);
            this.loading = false;
            this.showError('Error creating the album.');
        }
        });
    } catch (err) {
        console.error(err);
        this.loading = false;
        this.showError('Failed to convert files to Base64.');
    }
    }

    showError(message: string) {
        this.errorMessage = message;
        this.dialogType = 'error';
        this.dialogTitle = 'Validation Error';
        this.dialogMessage = message;
        this.showDialog = true;
    }

    showMessage(message: string) {
        this.dialogType = 'message';
        this.dialogTitle = 'Success';
        this.dialogMessage = message;
        this.showDialog = true;
    }

    closeDialog() {
        this.showDialog = false;
    }

    convertFileToBase64(file: File): Promise<string> {
        return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            const result = reader.result as string;
            const base64 = result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = error => reject(error);
        });
    }

    getArtistNameById(aId: string): string {
        const artist = this.artists.find(a => a.artistId === aId);
        return artist ? artist.name : aId;
    }
}
