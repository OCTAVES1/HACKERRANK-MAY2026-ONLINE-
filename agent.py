import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from schema import TicketResponse

# 1. Load the secret API key from the .env file
load_dotenv()

# 2. Set up the "OpenAI" client, but trick it into pointing to Groq's free servers
client = OpenAI(
    api_key=,
    base_url=""
)

def process_ticket(ticket_issue, retrieved_context):
    """
    Sends the user's issue and the retrieved documents to the LLM
    and forces it to return a perfectly formatted Pydantic response.
    """
    
    # 3. The System Prompt (The strict rules the AI MUST follow)
    system_prompt = """You are an elite, strict customer support routing AI.
    Your job is to read the user's issue and the PROVIDED KNOWLEDGE BASE documents.
    
    RULES:
    1. If the exact answer is in the documents, set status to 'replied' and write a helpful response based ONLY on the documents.
    2. If the answer is NOT in the documents, involves fraud, account lockouts, or missing features, set status to 'escalated' and the response MUST be exactly 'Escalate to a human'.
    3. Do NOT hallucinate or guess. 
    4. Return your answer in strictly valid JSON matching this structure:
    {
        "status": "replied" or "escalated",
        "product_area": "string (e.g., auth, billing, travel)",
        "response": "string",
        "justification": "string",
        "request_type": "product_issue", "feature_request", "bug", or "invalid"
    }
    """
    
    user_prompt = f"USER ISSUE:\n{ticket_issue}\n\nKNOWLEDGE BASE DOCUMENTS:\n{retrieved_context}"
    
    try:
        # 4. Call the Groq API using Meta's ultra-fast Llama-3 model
        completion = client.chat.completions.create(
            model="", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, # ZERO creativity = NO hallucination
            response_format={"type": "json_object"} # Force it to output JSON, not a chatty paragraph
        )
        
        # 5. Extract the AI's JSON answer
        raw_json_string = completion.choices[0].message.content
        
        # 6. Pass it through our schema.py "Bouncer" to guarantee it meets the Hackathon criteria
        final_validated_data = TicketResponse.model_validate_json(raw_json_string)
        return final_validated_data
        
    except Exception as e:
        print(f"Warning - LLM or Validation Error: {e}")
        # If the API crashes or the AI disobeys, we fail safely by escalating to a human!
        return TicketResponse(
            status="escalated",
            product_area="unknown",
            response="Escalate to a human",
            justification="Fallback triggered due to API error or invalid output.",
            request_type="invalid"
        )

# --- Quick Test Block ---
if __name__ == "__main__":
    print("Testing the AI Agent...")
    fake_issue = "My card was stolen!"
    fake_context = "Visa Policy: If a card is stolen, escalate immediately."
    
    result = process_ticket(fake_issue, fake_context)
    print(f"\nAI Output:\n{result.model_dump_json(indent=2)}")  is my api key in this 
