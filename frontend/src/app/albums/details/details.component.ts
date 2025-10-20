import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Album } from '../model/album.model';
import { AlbumService } from '../service/album.service';
import { TrackDTO } from '../model/album.model';
import { Artist } from '../../artists/model/artist.model';

@Component({
  selector: 'app-album-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css'],
  standalone: false
})
export class AlbumDetailsComponent implements OnInit {
    album!: Album;
    artists: Artist[] = [];
    audio = new Audio();
    currentTrack?: string;
    isPlaying = false;

    photoPath: string = 'photo.jpg';

    constructor(private route: ActivatedRoute, private albumService: AlbumService) {}

    ngOnInit() {
        const navState = history.state;

        if (navState.album) {
            this.album = navState.album;
            this.artists = navState.artists || [];
        } else {
            const albumId = this.route.snapshot.paramMap.get('id');
            if (albumId) {
                // this.albumService.getById(albumId).subscribe(album => {this.album = album;});
                this.album=this.albumService.getMock() //TODO: chamge to getById
            }
        }
    }

    getArtistNames(): string {
        if (!this.album?.artistIds?.length) return 'Unknown artist';
        return this.album.artistIds
        .map(id => this.artists.find(a => a.artistId === id)?.name || 'Unknown artist')
        .join(', ');
    }

    playTrack(track:TrackDTO) {
        if (!track.fileKey) return;

        if (this.isPlaying) {
            this.audio.pause();
            this.audio.currentTime = 0;
            this.isPlaying = false;
            return;
        }
        this.albumService.getUrl(track.fileKey).subscribe({
            next: (url) => {
                this.audio.src = url.url;
                this.audio.crossOrigin = 'anonymous';
                this.audio.load();
                this.audio.play().then(() => {
                    this.isPlaying = true;
                }).catch(err => console.error('Audio play failed:', err));

                this.audio.onended = () => this.isPlaying = false;
            },
            error: (err) => console.error('Failed to get track URL', err)
        });
    }

}
