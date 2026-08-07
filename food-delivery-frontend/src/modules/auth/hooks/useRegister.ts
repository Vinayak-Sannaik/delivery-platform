import { useMutation } from "@tanstack/react-query";

import {
  signup,
  type SignupRequest,
  type SignupResponse,
} from "../api/auth.api";

export function useRegister() {
  return useMutation<
    SignupResponse,
    Error,
    SignupRequest
  >({
    mutationFn: signup,
  });
}