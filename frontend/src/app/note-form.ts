import { Component, output } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { NewNote } from './note';

@Component({
  selector: 'app-note-form',
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <input formControlName="title" placeholder="Title" maxlength="120">
      <input formControlName="text" placeholder="Text">
      <button type="submit" [disabled]="form.invalid">Create</button>
    </form>
  `,
})
export class NoteForm {
  readonly created = output<NewNote>();

  protected readonly form = new FormGroup({
    title: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
    text: new FormControl('', { nonNullable: true }),
  });

  protected submit(): void {
    this.created.emit(this.form.getRawValue());
    this.form.reset();
  }
}
