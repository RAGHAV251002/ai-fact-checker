from services.search_service import search_claim
from services.verification_service import verify_claim

claim = "OpenAI has 500 million weekly active users."

search = search_claim(claim)

result = verify_claim(

    claim,

    search["answer"]

)

print(result)