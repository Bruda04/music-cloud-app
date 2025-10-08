export interface Song {
    songId?: string,
    title: string,
    artistIds: string[],
    genres: string[],
    fileContentBase64:string,
    other?: Record<string,string>,
}