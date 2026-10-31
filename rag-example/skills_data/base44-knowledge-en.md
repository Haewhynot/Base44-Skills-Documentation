# Base44 knowledge: learning Knowledge vs learning Skills

Base44 clearly separates what the AI learns as Knowledge from what it learns as action Skills.

## 1. Knowledge Base (learning knowledge)

Base44 DOES support learning knowledge from uploaded files.

- Supported formats: text documents such as PDF, Word and TXT.
- How it works: you upload documents directly into the Knowledge Base of the AI Chatbot integrated in your Base44 app.
- Purpose: the AI reads, scans and learns from these files so it can answer end-user questions automatically.

## 2. Super Agent Skills (learning action skills)

Base44 mainly accepts skills through prompts (descriptive text). Direct upload of logic-structure files is not currently supported.

- Base44 provides "Super Agents" that run in the background 24/7 to automate complex workflows.
- To teach a new skill or set operating rules for an agent, you describe the task in text (a prompt).
- Current limitation: the platform does not yet let you upload a logic-structure file (JSON or MD containing logic) for the agent to turn into an executable skill.

## 3. Agent Skills files in development (DX)

In the Base44 developer community, "uploading skills" is mostly about improving the developer experience, not loading them into the Base44 platform.

- A skill file (for example `SKILL.md`) is a pre-optimized documentation set containing `base44-sdk` or `base44-cli` context.
- Deployment: load it into the workspace of an AI IDE or assistant, not into Base44.
  - Cursor: use Project Knowledge or the `.cursorrules` file (or `.cursor/rules/*.mdc`).
  - Claude or Qoder: use Project Knowledge or the context window.

### Benefits of loading a skill file into your IDE

1. It teaches the AI the real structure of the Base44 framework.
2. It generates code that follows Base44 SDK and CLI standards.
3. It reduces hallucination: fewer invented functions that do not exist.
4. It helps with API integrations: Supabase, GitHub, Drive API, Google Calendar API.

## 4. Quick Q&A

**Q: Can Base44 learn skills from an uploaded file?**
A: It depends on the type. The Knowledge Base CAN learn from uploaded files (PDF, Word, TXT). Super Agent Skills work mainly through prompts and do not yet accept direct upload of logic files.

**Q: Where should I upload a SKILL.md file?**
A: Load it into a coding tool such as Cursor, Claude or Qoder so the AI writes more accurate Base44 code. Do not upload it to the Base44 platform as an agent skill.
