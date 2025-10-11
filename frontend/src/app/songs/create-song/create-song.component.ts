import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DialogType } from '../../shared/dialog/dialog.component';
import { Song } from '../model/song.model';
import { SongService } from '../service/song.service';
import { ArtistService } from '../../artists/service/artist.service';
import { Artist } from '../../artists/model/artist.model';
import { GenreService } from '../service/genre.service';
import { Genre } from '../model/genre.model';

@Component({
  selector: 'app-create-song',
  templateUrl: './create-song.component.html',
  styleUrls: ['../../shared/themes/forms.css'],
  standalone:false
})
export class CreateSongComponent implements OnInit{
  editMode = false;

  song: Song = {
    title: '',
    artistIds: [],
    genres: [],
    file:'',
    other:{}
  };

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

  constructor(private songService: SongService, private artistService:ArtistService, private genreService:GenreService, private router: Router,private route: ActivatedRoute) {}

  ngOnInit(){
    // this.artistService.getAll().subscribe(a=> this.artists = a);
    this.artists = this.artistService.getAllMock(); // TODO: change to getAll, its like this so i dont use all aws free requests
    // this.genreService.getAll().subscribe(g => this.genres = g);
    this.genres = this.genreService.getAllMock(); // TODO: change to getAll, its like this so i dont use all aws free requests
    const songId = this.route.snapshot.paramMap.get('id');
    if (songId) {
      this.editMode = true;
      // this.songService.getById(songId).subscribe(song => {
      //   this.song = song;
      // });
      this.song=this.songService.getMockById(); //TODO: change to getById
    }
  }

  addGenre() {
    const selected = this.genreInput.trim();
    const manual = this.genreInputManual.trim();
    const value = selected || manual;

    if (value && !this.song.genres.includes(value)) {
      this.song.genres.push(value);
      this.genreInput = '';
      this.genreInputManual = '';
    }
  }

  removeGenre(index: number) {
    this.song.genres.splice(index, 1);
  }

  addArtist() {
    if (this.artistInput.trim() && !this.song.artistIds.includes(this.artistInput)) {
      this.song.artistIds.push(this.artistInput.trim());
      this.artistInput = '';
    }
  }

  removeArtist(index: number) {
    this.song.artistIds.splice(index, 1);
  }

  addOther() {
    if (this.otherKey.trim()) {
      this.song.other![this.otherKey.trim()] = this.otherValue;
      this.otherKey = '';
      this.otherValue = '';
    }
  }

  removeOther(key: string) {
    delete this.song.other![key];
  }

  async submit() {
    if (!this.song.title.trim() || this.song.artistIds.length === 0 || this.song.genres.length === 0) {
      this.errorMessage = 'Title and at least one Artist and Genre are required';
      this.dialogType = 'error';
      this.dialogTitle = 'Validation Error';
      this.dialogMessage = this.errorMessage;
      this.showDialog = true;
      return;
    }

    if (!this.editMode && !this.uploadedFile) {
      this.errorMessage = 'You must upload an mp3 file';
      this.dialogType = 'error';
      this.dialogTitle = 'Validation Error';
      this.dialogMessage = this.errorMessage;
      this.showDialog = true;
      return;
    }

    this.loading = true;

    try {
      if (this.uploadedFile) {
        this.song.file = await this.convertFileToBase64(this.uploadedFile);
        this.song.fileChanged = true;
      } else {
        this.song.fileChanged = false;
      }

      console.log(this.song)
      const req = this.editMode ? this.songService.edit(this.song): this.songService.create(this.song);
      req.subscribe({
        next: res => {
          this.loading = false;
          this.dialogType = 'message';
          this.dialogTitle = 'Success';
          this.dialogMessage = res.message;
          this.showDialog = true;
        },
        error: err => {
          console.error(err);
          this.loading = false;
          this.dialogType = 'error';
          this.dialogTitle = 'Error';
          this.dialogMessage = 'Error request.';
          this.showDialog = true;
        }
      });
    } catch (err) {
      console.error(err);
      this.loading = false;
      this.dialogType = 'error';
      this.dialogTitle = 'Error';
      this.dialogMessage = 'Failed to convert file to Base64.';
      this.showDialog = true;
    }
  }

  closeDialog() {
    this.showDialog = false;
  }

  getArtistNameById(aId: string): string {
    const artist = this.artists.find(a => a.artistId === aId);
    return artist ? artist.name : aId;
  }

  uploadedFile?: File;
  dragging = false;

  onFileDropped(event: DragEvent) {
    event.preventDefault();
    this.dragging = false;
    if (event.dataTransfer && event.dataTransfer.files.length > 0) {
      this.uploadedFile = event.dataTransfer.files[0];
    }
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.uploadedFile = file;
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.dragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    this.dragging = false;
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

}
