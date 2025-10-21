export interface SubscriptionResponse {
  genres: string[];
  artists: { artistId: string; name: string }[];
}
