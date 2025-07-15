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
git clone https://github.com/your-username/ai-travel-planner.git
cd ai-travel-planner
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file with your keys:

```
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
```

---

## ▶️ Run

**Start backend:**

```bash
uvicorn main:app --reload
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

