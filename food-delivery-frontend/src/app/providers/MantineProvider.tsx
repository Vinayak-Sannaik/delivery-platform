import {
  MantineProvider as Provider,
} from "@mantine/core";

import { Notifications } from "@mantine/notifications";
import type { ReactNode } from "react";
import { theme } from "../theme/theme";

type Props = {
  children: ReactNode;
};

export default function MantineProvider({ children }: Props) {
  return (
    <Provider theme={theme}>
      <Notifications />

      {children}
    </Provider>
  );
}