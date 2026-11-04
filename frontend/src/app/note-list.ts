import { DatePipe } from '@angular/common';
import { Component, input, output } from '@angular/core';

import { Note } from './note';

@Component({
  selector: 'app-note-list',
  imports: [DatePipe],
  template: `
    <ul>
      @for (note of notes(); track note.id) {
        <li>
          <b>{{ note.title }}</b> {{ note.text }}
          <small>{{ note.created_at | date: 'short' }}</small>
          <button type="button" (click)="deleted.emit(note.id)">Delete</button>
        </li>
      } @empty {
        <li>No notes yet.</li>
      }
    </ul>
  `,
})
export class NoteList {
  readonly notes = input.required<Note[]>();
  readonly deleted = output<string>();
}
