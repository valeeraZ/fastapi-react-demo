"use client";
import {
  Button,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  useDisclosure,
} from "@nextui-org/react";
import { useState } from "react";
import { createContact } from "../lib/api";
import { ContactCreate } from "../types";

export default function CreateContactForm() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [job, setJob] = useState("");
  const [address, setAddress] = useState("");
  const [question, setQuestion] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const contact_create_form: ContactCreate = {
      first_name: firstName,
      last_name: lastName,
      job: job,
      address: address,
      question: question,
    };
    await createContact(contact_create_form);
    setFirstName("");
    setLastName("");
    setJob("");
    setAddress("");
    setQuestion("");
    window.location.reload();
  };



  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  const isDisable = !firstName || !lastName || !job || !address || !question;

  return (
    <>
      <Button onPress={onOpen} color="primary">
        New Contact
      </Button>
      <Modal isOpen={isOpen} onOpenChange={onOpenChange} placement="top-center">
        <ModalContent>
          {(onClose) => (
            <>
              <form onSubmit={handleSubmit}>
                <ModalHeader className="flex flex-col gap-1">
                  Create New Contact
                </ModalHeader>

                <ModalBody>
                  <Input
                    autoFocus
                    label="First Name"
                    placeholder="Enter your firstname"
                    variant="bordered"
                    onChange={(e) => setFirstName(e.target.value)}
                    isRequired
                  />
                  <Input
                    label="Last Name"
                    placeholder="Enter your lastname"
                    variant="bordered"
                    onChange={(e) => setLastName(e.target.value)}
                    isRequired
                  />
                  <Input
                    label="Job"
                    placeholder="Enter your job"
                    variant="bordered"
                    onChange={(e) => setJob(e.target.value)}
                    isRequired
                  />
                  <Input
                    label="Address"
                    placeholder="Enter your address"
                    variant="bordered"
                    onChange={(e) => setAddress(e.target.value)}
                    isRequired
                  />
                  <Input
                    label="Question"
                    placeholder="Enter your question"
                    variant="bordered"
                    onChange={(e) => setQuestion(e.target.value)}
                    isRequired
                  />
                </ModalBody>

                <ModalFooter>
                  <Button color="danger" variant="flat" onPress={onClose}>
                    Close
                  </Button>
                  <Button color="primary" type="submit" onPress={onClose} isDisabled={isDisable}>
                    Create
                  </Button>
                </ModalFooter>
              </form>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}
