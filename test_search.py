from services.search_service import search_claim

result = search_claim(
    "OpenAI has 500 million weekly active users"
)

print(result)