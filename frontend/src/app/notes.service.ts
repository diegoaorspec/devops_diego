import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { NewNote, Note } from './note';

@Injectable({ providedIn: 'root' })
export class NotesService {
  private readonly http = inject(HttpClient);
  private readonly url = '/api/v1/notes';

  list(): Observable<Note[]> {
    return this.http.get<Note[]>(this.url);
  }

  create(note: NewNote): Observable<Note> {
    return this.http.post<Note>(this.url, note);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
