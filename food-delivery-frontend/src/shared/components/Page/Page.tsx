import { Stack } from "@mantine/core";
import type { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export default function Page({
  children,
}: Props) {
  return (
    <Stack
      gap="xl"
      p="lg"
    >
      {children}
    </Stack>
  );
}