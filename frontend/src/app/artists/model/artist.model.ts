export interface Artist {
    artistId?:string,
    name: string,
    bio: string,
    genres: string[],
    other?: Record<string,string>
}