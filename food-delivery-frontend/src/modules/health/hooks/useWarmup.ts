import { useMutation } from "@tanstack/react-query";

import { warmupServices } from "../api/warmup.api";


export function useWarmup() {
  return useMutation({
    mutationFn: warmupServices,
  });
}