export interface Note {
  id: string;
  title: string;
  text: string;
  created_at: string;
}

export interface NewNote {
  title: string;
  text: string;
}
