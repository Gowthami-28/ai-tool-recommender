# AI Tool Recommender Agent

I run a YouTube channel where I test AI tools for business owners. Every week 
the same question comes up: "Which AI tool should I actually use for my 
problem?" I built this agent to answer that — describe your business problem 
in plain language, get back 3 specific tool recommendations with real reasons 
why each one fits.

Built during the Kaggle x Google 5-Day AI Agents Intensive, June 2026.

## What It Does

You type a business problem. The agent analyzes it, identifies the core 
challenge, and recommends 3 specialized AI tools — not the obvious ones 
everyone already knows, but tools that actually fit the specific problem.

I tested it with a bakery owner spending 3 hours on WhatsApp, a restaurant 
owner drowning in review responses, and a boutique owner manually creating 
Instagram posts every week. Each got different, relevant recommendations.

## How to Run It

### 1. Clone the repo

```bash
git clone https://github.com/Gowthami-28/ai-tool-recommender.git
cd ai-tool-recommender
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key

Create a file called `.env` inside the `ai_tool_recommender/` folder:
GOOGLE_API_KEY=your_key_here
**Never commit your API key.** The `.gitignore` already excludes `.env`.

### Running the Agent

**Option 1 — Python directly:**
```bash
python ai_tool_recommender/agent.py
```

**Option 2 — ADK CLI (recommended):**
```bash
adk run ai_tool_recommender
```

Then describe your business problem when prompted.

## Example Queries to Try

- "I own a restaurant and spend hours responding to customer reviews online"
- "I run a clothing boutique and create Instagram posts manually every week"
- "I manage a small gym and struggle to track member attendance"

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK 2.3.0 |
| Model | Gemini 2.5 Flash |
| IDE | Antigravity |
| Language | Python 3.12 |

## Built For

Kaggle x Google — AI Agents: Intensive Vibe Coding Capstone (July 2026)  
Track: **Agents for Business**

## Author

Gowthami Vanga — [GitHub](https://github.com/Gowthami-28)
