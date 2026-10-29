# SKILLS DOCUMENTATION: BASE44 AGENT SKILLS & KNOWLEDGE BASE

*Standard reference document for AI Assistants (Cursor, Claude, Qoder) on how Base44 processes data and skills.*

## 📌 1. Distinguishing Data Learning Features on Base44

The Base44 system clearly separates the learning process based on the user's intended purpose: Knowledge Learning and Skills Learning.

### 1.1. Knowledge Base Learning

* **Capability:** YES, supports direct learning from uploaded files.
* **Supported Formats:** Text documents (PDF, Word, TXT, etc.).
* **How it works:** Users upload documents directly into the Knowledge Base system of the AI Chatbot integrated within the Base44 application.
* **Purpose:** The AI reads, scans, and learns data from these files to build a knowledge base, automatically answering end-user queries.

### 1.2. Action Skills Learning (Super Agent Skills)

* **Capability:** PRIMARILY accepted via Prompts (descriptive text), DOES NOT CURRENTLY support direct uploads of logical structure files.
* **How it works:** Base44 utilizes "Super Agents" running in the background 24/7 to automate workflows. To teach a new skill or set operating rules for an Agent, the user must describe the task using text (prompts).
* **Current Limitations:** The Base44 platform does not yet allow direct uploads of logical structure files (like JSON or MD containing logic) for the agent to automatically convert into executable skills.

## 🚀 2. Practical Application of "Agent Skills" Files (Best Practices)

In the Base44 developer community, the concept of "uploading skills" is more about enhancing the Developer Experience (DX) than injecting them directly into the platform.

### 2.1. Nature of Agent Skills Files

* Skill files (e.g., `SKILL.md`) are typically pre-optimized documentation sets containing **base44-sdk** or **base44-cli** contexts.

### 2.2. Deployment Method

Instead of uploading to the Base44 platform, Developers load these files into the workspaces of AI IDEs/Assistants:

* **Cursor IDE:** Loaded via the Project Knowledge feature or the `.cursorrules` file.
* **Claude / Qoder:** Loaded into the Project Knowledge / Context window.

### 2.3. Benefits of AI IDE Integration

Integrating the `Skills.md` file into your IDE provides the following technical advantages:

1. **Teach AI:** Helps the AI Assistant accurately and comprehensively grasp the Base44 framework structure.
2. **Accurate Code Generation:** Assists the IDE in generating code that adheres strictly to the Base44 SDK/CLI standards.
3. **Anti-Hallucination:** Minimizes the risk of the AI inventing non-existent functions when configuring complex integrations.
4. **API Integration Support:** Especially useful when coding automation flows that connect to:
   * Supabase
   * GitHub
   * Drive API
   * Google Calendar API