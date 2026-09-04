import {apiClient} from "../../../shared/api/client";

export interface ChatRequest {
  conversation_id?: string | null;
  message: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
}

export const sendChatMessage = async (
  request: ChatRequest
): Promise<ChatResponse> => {
  const response = await apiClient.post<ChatResponse>(
    "/api/ai/chat",
    request
  );

  return response.data;
};