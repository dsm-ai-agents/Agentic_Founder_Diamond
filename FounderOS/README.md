# FounderOS: Hermes Team Chat Blueprint

This blueprint defines the internal AI operating system setup for Agentic Founder / Data Science Masterminds using Contabo, Coolify, Hermes, Hermes Web UI, LibreChat, ChatGPT OAuth, Composio MCP, and PostgreSQL.

## 1. Goal

Create a private company AI assistant where team members can ask business questions, access approved knowledge, and eventually trigger business actions, while Hermes remains the central brain.

The key principle:

```text
LibreChat / Slack / WhatsApp / Web UI = interfaces
Hermes = brain and orchestration layer
PostgreSQL = memory and knowledge storage
Composio = MCP tool/action layer
```

## 2. Core Stack

| Layer | Tool |
|---|---|
| Server | Contabo VPS |
| Deployment | Coolify |
| AI Brain | Hermes |
| Team Chat UI | LibreChat |
| CEO/Admin UI | Hermes Web UI |
| LLM Access | ChatGPT OAuth / OpenRouter |
| MCP Tools | Composio |
| Database | PostgreSQL via Coolify |
| Memory | PostgreSQL + pgvector + graph memory tables |
| Automation | n8n optional |
| Team Access | LibreChat login |

## 3. Main Architecture

```text
Team Member
   ↓
LibreChat
   ↓
Hermes API
   ↓
Hermes Brain
   ↓
Permission Check
   ↓
Chat Memory + Graph Memory + Knowledge Base
   ↓
ChatGPT / OpenRouter
   ↓
Composio MCP Tools
   ↓
Response back to LibreChat
```

## 4. Role of Each Component

### Contabo

Contabo hosts the VPS where the full stack runs.

```text
Contabo VPS
   ↓
Coolify
   ↓
LibreChat + Hermes + PostgreSQL + n8n
```

### Coolify

Coolify deploys and manages:

```text
Hermes
LibreChat
PostgreSQL
n8n
Redis if needed
Background workers
```

### LibreChat

LibreChat is the team-facing ChatGPT-style interface.

Team members can ask:

```text
What is our current pricing?
Where is the SOP?
Generate a proposal.
What should I reply to this lead?
What is the onboarding process?
```

LibreChat should not own the business brain. It should act as the frontend only.

### Hermes

Hermes is the intelligence and orchestration layer.

Hermes handles:

```text
User identity
Role permissions
Memory
Knowledge retrieval
Tool calling
Business logic
Final response generation
```

### Hermes Web UI

Hermes Web UI is for CEO/admin usage.

Use it to:

```text
Manage knowledge
View conversations
Manage users
Add tools
Review memory
Debug agent behavior
Approve sensitive actions
```

### ChatGPT OAuth / OpenRouter

Used by Hermes to access models.

Recommended setup:

```text
Testing: ChatGPT / OpenAI
Production: OpenRouter
```

### Composio MCP

Composio becomes the tool/action layer.

Hermes can use Composio to access:

```text
Google Drive
Gmail
Google Calendar
Slack
Notion
GitHub
CRM
Sheets
Docs
```

## 5. PostgreSQL Database Design

Create the following tables:

```text
users
roles
permissions
chat_sessions
chat_messages
user_memory
business_memory
knowledge_documents
knowledge_chunks
memory_nodes
memory_edges
tool_logs
```

## 6. Chat Memory

Chat memory stores normal conversation history.

```text
User asks question
Hermes saves user message
Hermes generates response
Hermes saves assistant response
```

Example:

```text
Raj asked about pricing.
Hermes replied with current pricing.
Next time Raj says “summarize that”, Hermes understands the context.
```

## 7. Long-Term Memory

Long-term memory stores important facts that should persist beyond one chat.

Examples:

```text
Raj is part of sales.
Anisha handles delivery.
Deepika manages operations.
The AI Agent Accelerator price is ₹X.
The refund policy is Y.
```

This should not store every chat message. It should store useful business memory only.

## 8. Graph Memory

Graph memory can be added as an Obsidian-style relationship layer.

Recommended principle:

```text
PostgreSQL = actual memory database
Obsidian-style graph = visual thinking layer
```

Graph memory stores relationships like:

```text
Kunaal → owns → Data Science Masterminds
DSM → sells → AI Agent Accelerator
AI Agent Accelerator → includes → n8n
n8n → connects_to → WhatsApp API
Raj → works_in → Sales
Sales → uses → Pricing SOP
```

## 9. Graph Memory Tables

### memory_nodes

```sql
create table memory_nodes (
  id uuid primary key default gen_random_uuid(),
  node_type text,
  name text,
  description text,
  metadata jsonb,
  created_at timestamp default now(),
  updated_at timestamp default now()
);
```

### memory_edges

```sql
create table memory_edges (
  id uuid primary key default gen_random_uuid(),
  source_node_id uuid references memory_nodes(id),
  target_node_id uuid references memory_nodes(id),
  relationship text,
  strength numeric default 1,
  metadata jsonb,
  created_at timestamp default now()
);
```

Example:

```text
Node: AI Agent Accelerator
Node: n8n
Edge: AI Agent Accelerator uses n8n
```

## 10. Obsidian Integration

Obsidian can be used in two ways.

### Option A: View-only Obsidian

Hermes exports important memory into Markdown files.

Example structure:

```text
/obsidian-vault/
   /people/Raj.md
   /products/AI Agent Accelerator.md
   /sops/Sales Process.md
   /clients/ANSR.md
```

Each file can have backlinks:

```markdown
# AI Agent Accelerator

Related:
- [[n8n]]
- [[OpenRouter]]
- [[Composio]]
- [[Sales SOP]]
```

This gives a visual knowledge graph.

### Option B: Obsidian as Knowledge Source

Business notes are maintained in Obsidian.

Hermes reads the vault, chunks it, embeds it, and stores it in PostgreSQL.

```text
Obsidian Notes
   ↓
Hermes Sync
   ↓
PostgreSQL / pgvector
   ↓
Hermes Answers
```

Best option:

```text
Use Obsidian for human thinking.
Use PostgreSQL for AI memory.
```

## 11. Permission System

Every user gets a role.

```text
CEO
Sales
Marketing
Delivery
Operations
Intern
Customer Support
```

Each role gets allowed knowledge.

Example:

```text
Sales can access:
- Pricing
- Offers
- Lead SOP
- Proposal templates

Delivery can access:
- Training SOP
- Course material
- Student onboarding

Intern can access:
- Public docs
- Task SOPs

CEO can access:
- Everything
```

Hermes checks permissions before answering.

## 12. Message Flow

```text
1. Team member logs into LibreChat
2. User sends question
3. LibreChat sends message to Hermes API
4. Hermes identifies user
5. Hermes checks role and permissions
6. Hermes loads recent chat memory
7. Hermes loads long-term memory
8. Hermes searches knowledge base
9. Hermes checks graph memory
10. Hermes calls tools through Composio if needed
11. Hermes generates answer
12. Hermes saves the conversation
13. Hermes returns response to LibreChat
```

## 13. Recommended Phased Setup

### Phase 1: Basic Team Chat

Add:

```text
Contabo
Coolify
LibreChat
Hermes
PostgreSQL
OpenRouter / ChatGPT
```

Goal:

```text
Team can chat with Hermes.
Hermes remembers conversations.
```

### Phase 2: Knowledge Base

Add:

```text
Google Drive
SOPs
PDFs
Docs
Training material
Pricing docs
```

Goal:

```text
Hermes answers from company documents.
```

### Phase 3: Role-Based Access

Add:

```text
Users
Roles
Permissions
Department access
```

Goal:

```text
Sales sees sales.
Delivery sees delivery.
CEO sees everything.
```

### Phase 4: Composio MCP Tools

Add:

```text
Gmail
Calendar
Drive
Sheets
Slack
CRM
```

Goal:

```text
Hermes can take actions.
```

### Phase 5: Graph Memory

Add:

```text
memory_nodes
memory_edges
entity extraction
relationship mapping
Obsidian export
```

Goal:

```text
Hermes understands business relationships, not just documents.
```

## 14. Final Recommended Blueprint

```text
Contabo VPS
   ↓
Coolify
   ↓
------------------------------------------------
| LibreChat          → Team Chat UI             |
| Hermes Web UI      → CEO/Admin UI             |
| Hermes API         → Brain + Orchestration    |
| PostgreSQL         → Chat + Memory + Graph    |
| pgvector           → Knowledge Search         |
| Composio MCP       → Tools and Actions        |
| OpenRouter/GPT     → LLM Brain                |
| n8n                → Workflow Automation      |
------------------------------------------------
```

## 15. Best Principle

Do not make LibreChat, Slack, WhatsApp, or Obsidian the brain.

Use them only as interfaces.

The real brain should be:

```text
Hermes + PostgreSQL + Graph Memory + MCP Tools
```

That way, tomorrow the same system can support:

```text
Slack
WhatsApp
Telegram
Customer Portal
Mobile App
```

without rebuilding the intelligence layer.
