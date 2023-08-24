import CreateContactForm from "./component/ContactCreateForm";
import ContactsList from "./component/ContactsList";
import { getContacts } from "./lib/api";

export default async function Home() {
  const contacts = await getContacts();

  return (
    <div className="px-4 py-12 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold mb-8">All Contacts</h1>
      <CreateContactForm />
      <div className="my-4">
        <ContactsList contacts={contacts} />
      </div>
    </div>
  );
}
