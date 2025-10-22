import { Injectable } from '@angular/core';

export interface CachedTrack {
  filename: string;
  data: string; // Base64 ili Blob URL
  timestamp: number;
}

@Injectable({
  providedIn: 'root'
})
export class CacheService {
  private readonly STORAGE_PREFIX = 'cache-';
  private readonly MAX_TRACKS = 2;

  constructor() {}

  private getAllKeys(): string[] {
    return Object.keys(localStorage).filter(k => k.startsWith(this.STORAGE_PREFIX));
  }

  saveTrack(trackId: string, filename: string, blob: Blob) {
    const reader = new FileReader();
    reader.onload = () => {
      const base64Data = reader.result as string;

      const cachedItem = {
        filename,
        data: base64Data,
        timestamp: Date.now()
      };

      const keys = this.getAllKeys();
      if (keys.length >= this.MAX_TRACKS) {
        const oldestKey = keys
          .map(k => ({ key: k, ts: JSON.parse(localStorage.getItem(k)!).timestamp }))
          .sort((a, b) => a.ts - b.ts)[0].key;
        localStorage.removeItem(oldestKey);
      }

      localStorage.setItem(this.STORAGE_PREFIX + trackId, JSON.stringify(cachedItem));
    };
    reader.readAsDataURL(blob);
  }

  getTrack(trackId: string) {
    const raw = localStorage.getItem(this.STORAGE_PREFIX + trackId);
    if (!raw) return null;
    return JSON.parse(raw) as { filename: string; data: string; timestamp: number };
  }

  isCached(trackId: string): boolean {
    return !!localStorage.getItem(this.STORAGE_PREFIX + trackId);
  }
}
