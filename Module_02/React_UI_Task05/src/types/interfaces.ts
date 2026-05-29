export interface Citation {
  source_uri: string;
  quote: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  text: string;
  streaming?: boolean;
  citations?: Citation[];
  confidence?: number;
  is_grounded?: boolean;
  user_aborted?: boolean;
}