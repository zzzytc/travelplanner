from langgraph.graph import MessageGraph
from dotenv import load_dotenv
from langgraph.graph import END
from typing import Sequence, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from chains import generate_chain, reflect_chain, query_chain
from langchain.tools.tavily_search import TavilySearchResults
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

load_dotenv()
app = FastAPI()
tavily_tool = TavilySearchResults()

def curate_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    user_inputs = [
        message.content for message in messages if isinstance(message, HumanMessage)
    ]
    user_input_combined = "\n".join(user_inputs)
    prompt = HumanMessage(
        content=(
            "Interpret the user's travel request and extract key planning criteria.\n"
            "Summarize the destination, purpose, preferences (e.g. food, culture), travel dates, budget,\n"
            "and any constraints. Use this to guide the rest of the planning.\n\n"
            f"{user_input_combined}"
        )
    )
    response = generate_chain.invoke({"messages": messages + [prompt]})

    return list(messages) + [response]

def flight_node(messages):
    query = query_chain.invoke({"messages":[messages[0].content + "Construct a search query to find flight for the origin and destination to put in the search engine."]})
    tavily_result = tavily_tool.invoke(query.content)
    prompt = f"Based on the following real-time flight info, suggest the best flight options:\n{tavily_result}"
    response = generate_chain.invoke({"messages": messages + [HumanMessage(content=prompt)]})

    
    result = messages + [response]
    return result

def budget_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    prompt = (
        "Evaluate the current travel plan and estimate the total cost.\n"
        "Check if the plan stays within the user's stated or inferred budget.\n"
        "If it exceeds the budget, suggest specific adjustments (e.g., cheaper hotels, fewer paid activities, use of public transport).\n"
        "Be transparent in your reasoning and propose a revised budget breakdown if needed."
    )

    response = generate_chain.invoke({"messages": messages + [HumanMessage(content=prompt)]})
    return list(messages) + [response]

def itinerary_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    prompt = (
        "Based on the user's preferences and the plan so far, generate a personalized daily itinerary.\n"
        "Include local experiences, food stops, cultural sites, and breaks.\n"
        "Make it well-paced, feasible, and aligned with the user's stated interests (e.g., temples, food, nature).\n"
        "Ensure the itinerary starts after arrival and ends before departure."
    )

    response = generate_chain.invoke({"messages": messages + [HumanMessage(content=prompt)]})
    return list(messages) + [response]


def hotel_node(messages):
    query = query_chain.invoke({"messages":[messages[0].content + "Construct a search query to find boutique hotel for the trip to put in the search engine."]})
    tavily_result = tavily_tool.invoke(query.content)
    prompt = f"Based on the following hotel info, recommend options aligned with user preferences:\n{tavily_result}"
    response = generate_chain.invoke({"messages": messages + [HumanMessage(content=prompt)]})

    return list(messages) + [response]


def summary_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    prompt = (
        "Please summarize the complete travel plan for the user, including:\n"
        "- Destination and travel dates\n"
        "- Flight details\n"
        "- Hotel/accommodation info\n"
        "- Daily itinerary highlights\n"
        "- Budget alignment\n"
        "Present the plan clearly and helpfully as if you're a travel consultant."
    )
    
    response = generate_chain.invoke({
        "messages": messages + [HumanMessage(content=prompt)]
    })

    return list(messages) + [response]


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    critique = reflect_chain.invoke({"messages": messages})
    return list(messages) + [critique]

graph = MessageGraph()

# === Add agent nodes ===
graph.add_node("curate", curate_node)
graph.add_node("reflect_curate", reflection_node)

graph.add_node("flights", flight_node)
graph.add_node("reflect_flights", reflection_node)

graph.add_node("hotels", hotel_node)
graph.add_node("reflect_hotels", reflection_node)

graph.add_node("itinerary", itinerary_node)
graph.add_node("reflect_itinerary", reflection_node)

graph.add_node("budget", budget_node)
graph.add_node("reflect_budget", reflection_node)

graph.add_node("summary", summary_node)


graph.set_entry_point("curate")

graph.add_edge("curate", "reflect_curate")
graph.add_edge("reflect_curate", "flights")

graph.add_edge("flights", "reflect_flights")
graph.add_edge("reflect_flights", "hotels")

graph.add_edge("hotels", "reflect_hotels")
graph.add_edge("reflect_hotels", "itinerary")

graph.add_edge("itinerary", "reflect_itinerary")
graph.add_edge("reflect_itinerary", "budget")

graph.add_edge("budget", "reflect_budget")
graph.add_edge("reflect_budget", "summary")

graph.add_edge("summary", END)

compiled_app = graph.compile()

class TravelRequest(BaseModel):
    query: str

# === FastAPI Endpoints ===
@app.post("/travel-plan")
async def generate_travel_plan(request: TravelRequest):
    try:
        result = compiled_app.invoke([HumanMessage(content=request.query)])
        summary = result[-1]
        print(f"######################{summary}")
        return JSONResponse(content={"messages": summary.content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Planning API! Use /travel-plan to generate a plan."}