import {
  ActionIcon,
  Button,
  Group,
  Stack,
  Text,
  TextInput,
} from "@mantine/core";
import { IconMessage, IconX } from "@tabler/icons-react";
import { useState } from "react";
import { sendChatMessage } from "../api/ai.api";

export default function AIChat() {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [response, setResponse] = useState("");

  const handleSend = async () => {
    if (!message.trim()) return;

    try {
      const result = await sendChatMessage({
        conversation_id: conversationId,
        message: message.trim(),
      });

      setConversationId(result.conversation_id);
      setResponse(result.message);
      setMessage("");
    } catch (error) {
      console.error("AI chat failed:", error);
    }
  };
  if (!open) {
    return (
      <ActionIcon
        size={60}
        radius="xl"
        onClick={() => setOpen(true)}
        style={{
          position: "fixed",
          right: 24,
          bottom: 24,
          zIndex: 1000,
        }}
      >
        <IconMessage size={28} />
      </ActionIcon>
    );
  }

  return (
    <Stack
      style={{
        position: "fixed",
        right: 24,
        bottom: 24,
        width: 350,
        padding: 16,
        zIndex: 1000,
        background: "white",
        borderRadius: 8,
        boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
      }}
    >
      <Group justify="space-between">
        <Text fw={600}>AI Assistant</Text>

        <ActionIcon variant="subtle" onClick={() => setOpen(false)}>
          <IconX size={18} />
        </ActionIcon>
      </Group>

      <TextInput
        placeholder="Ask me anything..."
        value={message}
        onChange={(event) => setMessage(event.currentTarget.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            handleSend();
          }
        }}
      />

      <Group justify="flex-end">
        <Button onClick={handleSend}>Send</Button>
      </Group>

      {response && <Text>{response}</Text>}
    </Stack>
  );
}
