"use client";
import { Accordion, AccordionItem, Avatar } from "@nextui-org/react";
import { ContactRead } from "../types";


export default function ContactsList({
  contacts: contacts,
}: {
  contacts: ContactRead[];
}) {
  return (
    <Accordion selectionMode="multiple">
      {contacts.map((contact) => (
        <AccordionItem
          key={contact.id}
          startContent={<Avatar name={contact.first_name.charAt(0).toUpperCase()} />}
          title={contact.first_name + " " + contact.last_name}
        >
          <p>
            <b>Address</b>: {contact.address}
          </p>
          <p>
            <b>Job</b>: {contact.job}
          </p>
          <p>
            <b>Question</b>: {contact.question}
          </p>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
