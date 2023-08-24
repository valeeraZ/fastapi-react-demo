// lib/api.ts

import axios from "axios";
import { ContactCreate, ContactRead } from "../types";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";

export async function getContacts(): Promise<ContactRead[]> {
  const url = `${API_URL}/contacts`;
  const response = await axios.get(url);
  return response.data;
}

export async function getContactById(id: number): Promise<ContactRead> {
  const url = `${API_URL}/contacts/${id}`;
  const response = await axios.get(url);
  return response.data;
}

export async function createContact(
  contact: ContactCreate
): Promise<ContactRead> {
  const url = `${API_URL}/contacts`;
  const response = await axios.post(url, contact);
  return response.data;
}
