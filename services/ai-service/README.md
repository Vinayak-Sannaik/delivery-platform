Chat → LLM → search_menu tool → Catalog Service → response

User
 │
 │ "Show me something under ₹300"
 │
 ▼
AI Service
 │
 ▼
Groq
 │
 │ tool_call:
 │ search_menu({
 │    max_price: 300
 │ })
 │
 ▼
ToolExecutor
 │
 ▼
Catalog Service
 │
 ▼
PostgreSQL
 │
 ▼
Menu Items
 │
 ▼
AI Service
 │
 ▼
Groq
 │
 ▼
"I found 5 items under ₹300..."