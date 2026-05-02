from pydantic import BaseModel, Field
from typing import Literal

class TicketResponse(BaseModel):
    status: Literal["replied", "escalated"] = Field(
        description="Must strictly be 'replied' if we can answer using the docs, or 'escalated' if it requires human intervention, involves fraud, missing features, or account lockouts."
    )
    product_area: str = Field(
        description="The specific product category or domain area (e.g., 'auth', 'billing', 'screen', 'travel_support'). Infer this from the issue."
    )
    response: str = Field(
        description="The user-facing answer. If status is 'escalated', this MUST be exactly 'Escalate to a human'. If 'replied', it must be a helpful, formatted response grounded ONLY in the retrieved documents."
    )
    justification: str = Field(
        description="A concise internal explanation of why the AI chose to reply or escalate based on the rules."
    )
    request_type: Literal["product_issue", "feature_request", "bug", "invalid"] = Field(
        description="Classify the core nature of the user's request."
    )
