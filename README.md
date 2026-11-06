# ✈️ AI Travel Booking System

A multi-agent travel planner built with **LangGraph**. Describe a trip in plain English and four agents work in sequence to fetch flight data, shortlist hotels, build a day-by-day itinerary, and combine everything into one final plan. Conversations are checkpointed in **PostgreSQL**, and the UI is a **Streamlit** app with a custom "airmail" design.

> Example request: *"Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs"*

---

## Features

- **Multi-agent workflow**: Flight, Hotel, Itinerary and Final agents orchestrated as a LangGraph `StateGraph`
- **Live data**: flight information from AviationStack, hotel and travel research from Tavily Search
- **LLM-powered planning**: itinerary and final plan generated with Groq (`openai/gpt-oss-120b`)
- **Persistent memory**: graph state is checkpointed in PostgreSQL via `PostgresSaver`, keyed by a user/thread ID
- **Live agent streaming**: each agent's output appears in the UI as soon as it finishes
- **Starter destinations**: one-click prompts for Tokyo, Paris, Bangkok, Rome, Dubai and Bali
- **Export**: every plan is saved to `travel_plans/` as Markdown and can be downloaded from the UI
- **CLI mode**: run the same pipeline from the terminal

---

## How it works

```
START → Flight Agent → Hotel Agent → Itinerary Agent → Final Agent → END
```

| Agent | What it does | Powered by |
|-------|--------------|------------|
| **Flight Agent** | Fetches flight data (airline, departure, arrival, status) | AviationStack API |
| **Hotel Agent** | Searches for the best hotels for the request | Tavily Search |
| **Itinerary Agent** | Builds a travel itinerary from the query, flights and hotels | Groq LLM |
| **Final Agent** | Merges flights, hotels and itinerary into one response | Groq LLM |

All agents share a single typed state:

```python
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
```

---

## Tech stack

| Layer | Tools |
|-------|-------|
| Orchestration | LangGraph, LangChain |
| LLM | Groq (`langchain-groq`) |
| Search | Tavily |
| Flight data | AviationStack |
| Memory / checkpointing | PostgreSQL, `langgraph-checkpoint-postgres`, `psycopg` |
| Frontend | Streamlit |
| Config | python-dotenv |

---

## Project structure

```
.
├── app.py                 # Streamlit UI
├── main.py                # LangGraph workflow + CLI entry point
├── requirements.txt
├── .env                   # API keys (not committed)
├── tools/
│   ├── flight_tool.py     # AviationStack wrapper
│   └── tavily_tool.py     # Tavily search wrapper
└── travel_plans/          # Auto-saved plans (created at runtime)
```

---

## Getting started

### Prerequisites

- Python 3.10+
- A running PostgreSQL database
- API keys for [Groq](https://console.groq.com), [Tavily](https://tavily.com) and [AviationStack](https://aviationstack.com)

### 1. Clone and install

```bash
git clone <your-repo-url>
cd <your-repo-folder>

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/travel_db
GROK_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
```

> `GROK_API_KEY` holds your **Groq** key. That is the variable name the code reads.

### 3. Run

**Web app**

```bash
streamlit run app.py
```

**Command line**

```bash
python main.py
```

The first run creates the checkpoint tables in PostgreSQL automatically (`checkpointer.setup()`).

---

## Usage

1. Open the Streamlit app and enter a **User ID** in the sidebar. It is used as the LangGraph `thread_id`.
2. Click a destination stamp for a starter prompt, or type your own request.
3. Click **Generate my travel plan**.
4. Watch each agent report in, then read the final plan.
5. Download the plan as Markdown, or find it in `travel_plans/`.

---

## Known limitations

- The AviationStack free tier returns general flight listings and does not filter by route or date, so flight results are indicative rather than bookable fares.
- The agents run sequentially, so a request takes as long as the sum of its steps.
- The project plans trips but does not complete real bookings or payments.

## Roadmap

- [ ] Extract origin, destination and dates from the query and use them in the flight search
- [ ] Run the Flight and Hotel agents in parallel
- [ ] Add budget tracking and currency conversion
- [ ] Add a conversational follow-up mode ("make day 3 less busy")
- [ ] Deploy on Streamlit Cloud with a hosted Postgres database

---

## Author

Built by **Aarohi** as part of my data science and GenAI learning journey.
Feel free to open an issue or connect with me on LinkedIn.
