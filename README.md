# 🧭 AI Travel Planner

An AI-powered travel planner built with **LangGraph**, **FastAPI**, and **Gradio**. It interprets user travel requests and generates full itineraries with flights, hotels, budgets, and more.

---

## 🚀 Features

* Understands natural-language travel queries
* Suggests real-time flights and hotels (via Tavily)
* Builds personalized itineraries and budgets
* Offers reflection to improve plan quality
* Easy-to-use Gradio web UI

---

## 🛠️ Setup

```bash
git clone https://github.com/zzzytc/travelplanner.git
cd travelplanner
python -m venv demo && source demo/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your keys:

```
WATSONX_APIKEY=your_key
WATSONX_PROJECTID=your_key
TAVILY_API_KEY = your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true

```

---

## ▶️ Run

**Start backend:**

```bash
uvicorn backend:app --reload
```

**Start frontend:**

```bash
python gradio_app.py
```

---

## 📬 API Example

```http
POST /travel-plan
{ "query": "Plan a 5-day trip to Tokyo from Hong Kong" }
```

