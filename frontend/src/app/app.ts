import { Component, OnInit, inject, signal } from '@angular/core';

import { NewNote, Note } from './note';
import { NoteForm } from './note-form';
import { NoteList } from './note-list';
import { NotesService } from './notes.service';

@Component({
  selector: 'app-root',
  imports: [NoteForm, NoteList],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly notesService = inject(NotesService);

  protected readonly notes = signal<Note[]>([]);
  protected readonly error = signal('');

  ngOnInit(): void {
    this.load();
  }

  protected create(note: NewNote): void {
    this.notesService.create(note).subscribe({
      next: () => this.load(),
      error: () => this.error.set('Could not create the note.'),
    });
  }

  protected delete(id: string): void {
    this.notesService.delete(id).subscribe({
      next: () => this.load(),
      error: () => this.error.set('Could not delete the note.'),
    });
  }

  private load(): void {
    this.notesService.list().subscribe({
      next: (notes) => {
        this.notes.set(notes);
        this.error.set('');
      },
      error: () => this.error.set('The API is not responding.'),
    });
  }
}
