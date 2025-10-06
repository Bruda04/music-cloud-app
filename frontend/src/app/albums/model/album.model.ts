import { Artist } from "../../artists/model/artist.model";

export interface Album {
    name: string,
    artists: Artist[],
    genres: string[],
    imageUrl: string,
    songsUrls: string[],
    rating: number,
}