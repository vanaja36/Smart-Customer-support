# pyre-ignore-all-errors
from pydantic import BaseModel  # pyre-ignore[21]
from typing import List, Optional, Literal, Dict, Any

class Ticket(BaseModel):
    id: str
    message: str
    category: str = ""
    response: str = ""
    status: Literal["open", "closed"] = "open"

class Observation(BaseModel):
    open_tickets: List[Ticket] = []
    last_action_result: str = ""

class Action(BaseModel):
    action_type: Literal["classify", "respond", "close", "wait"]
    ticket_id: str
    text_content: Optional[str] = None

class Reward(BaseModel):
    value: float = 0.0
    reason: str = ""

class CustomerSupportEnv:
    def __init__(self, tickets: List[Ticket], target_categories: Dict[str, str], target_responses: Dict[str, str]):
        self.initial_tickets = tickets
        self.tickets = []
        self.target_categories = target_categories
        self.target_responses = target_responses
        self.step_count = 0
        self.max_steps = 20

    def reset(self) -> Observation:
        self.tickets = [t.model_copy() for t in self.initial_tickets]
        self.step_count = 0
        return self._get_obs("Environment reset.")

    def _get_obs(self, result: str) -> Observation:
        open_tickets = [t for t in self.tickets if t.status == "open"]
        return Observation(open_tickets=open_tickets, last_action_result=result)

    def state(self) -> Dict[str, Any]:
        return {
            "tickets": [t.model_dump() for t in self.tickets],
            "step_count": self.step_count
        }

    def step(self, action: Action):
        self.step_count += 1
        reward_value = 0.0
        reward_reason = ""
        done = False
        result = ""

        if action.action_type == "wait":
            return self._get_obs("Waiting..."), Reward(value=-0.05, reason="Idle penalty"), False, {"reason": "Idle"}

        ticket = next((t for t in self.tickets if t.id == action.ticket_id), None)
        
        if not ticket:
            reward_value -= 0.1
            reward_reason = "Invalid ticket ID."
            result = "Error: Invalid ticket ID."
        elif ticket.status == "closed":
            reward_value -= 0.1
            reward_reason = "Ticket is already closed."
            result = "Error: Ticket already closed."
        else:
            if action.action_type == "classify":
                if ticket.category != "":
                    reward_value -= 0.05
                    reward_reason = "Ticket already classified."
                    result = "Error: Already classified."
                else:
                    ticket.category = action.text_content or ""
                    if self.target_categories.get(ticket.id) == ticket.category:
                        reward_value += 0.2
                        reward_reason = "Correct classification."
                        result = f"Ticket {ticket.id} classified as {ticket.category}."
                    else:
                        reward_value -= 0.1
                        reward_reason = "Incorrect classification."
                        result = f"Ticket {ticket.id} classified incorrectly."
                        
            elif action.action_type == "respond":
                if ticket.response != "":
                    reward_value -= 0.05
                    reward_reason = "Ticket already responded to."
                    result = "Error: Already responded."
                elif ticket.category == "":
                    reward_value -= 0.1
                    reward_reason = "Must classify before responding."
                    result = "Error: Classify first."
                else:
                    if action.text_content and len(action.text_content.strip()) > 5:
                        ticket.response = action.text_content
                        reward_value += 0.3
                        reward_reason = "Response drafted."
                        result = f"Response added to {ticket.id}."
                    else:
                        reward_value -= 0.1
                        reward_reason = "Invalid or empty response."
                        result = "Error: Invalid response."
                        
            elif action.action_type == "close":
                if ticket.category != "" and ticket.response != "":
                    ticket.status = "closed"
                    reward_value += 0.5
                    reward_reason = "Ticket successfully closed."
                    result = f"Ticket {ticket.id} closed."
                else:
                    reward_value -= 0.2
                    reward_reason = "Cannot close without category and response."
                    result = "Error: Incomplete ticket."

        open_tickets = [t for t in self.tickets if t.status == "open"]
        if not open_tickets:
            done = True
            result += " All tickets processed!"
            
        if self.step_count >= self.max_steps:
            done = True
            reward_reason += " Max steps reached."
            result += " Max steps reached."

        reward = Reward(value=reward_value, reason=reward_reason)
        return self._get_obs(result), reward, done, {"reason": reward_reason}
