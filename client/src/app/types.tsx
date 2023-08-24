export interface ContactRead {
  id: number;
  first_name: string;
  last_name: string;
  job: string;
  address: string;
  question: string;
}

export interface ContactCreate {
  first_name: string;
  last_name: string;
  job: string;
  address: string;
  question: string;
}
