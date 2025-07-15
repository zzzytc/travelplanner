from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ibm import ChatWatsonx
import os
from dotenv import load_dotenv

load_dotenv()
WATSONX_APIKEY = os.getenv('WATSONX_APIKEY')
WATSONX_PROJECTID = os.getenv('WATSONX_PROJECTID')

# 🔹 Prompt for generating a travel plan (e.g., itinerary, suggestions)
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional travel planner creating personalized travel plans for clients."
            " Given the user's preferences, budget, and travel dates, suggest a high-quality travel plan."
            " Be specific, creative, and align with the user's goals (e.g. food, nature, culture).",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# 🔹 Prompt for reflecting on a travel plan
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a critical travel reviewer analyzing a proposed travel plan."
            " Evaluate whether the plan satisfies the user's stated preferences (e.g., food-focused, nature-focused),"
            " adheres to budget, avoids impractical scheduling (e.g., long flights before early tours), and balances the itinerary."
            " List any issues, then suggest specific improvements. Be constructive, detailed, and professional.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

query_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a query generation expert. Your job is to convert a user's natural language request "
     "into a precise and effective web search query. Focus on extracting location, time, price, and intent. "
     "Keep the query short, specific, and optimized for search engines like Google or tools like Tavily.\n\n"
     "Do not include filler words or full sentences. Just return the query string."),
    MessagesPlaceholder(variable_name="messages")
])

# 🔹 Define LLM
llm = ChatWatsonx(
    model_id="meta-llama/llama-3-405b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id=WATSONX_PROJECTID,
    apikey=WATSONX_APIKEY,
    params={
        "max_new_tokens": 500,
        "min_new_tokens": 1,
        "temperature": 0.7,
    },
)

generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm
query_chain = query_prompt | llm