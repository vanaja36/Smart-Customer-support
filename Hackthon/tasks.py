from env import CustomerSupportEnv, Ticket

class BaseTask:
    def evaluate(self, env: CustomerSupportEnv) -> float:
        raise NotImplementedError

class EasyTask(BaseTask):
    def __init__(self):
        tickets = [Ticket(id="T1", message="My password is not working.")]
        target_cat = {"T1": "login_issue"}
        target_resp = {"T1": "reset"}
        self.env = CustomerSupportEnv(tickets, target_cat, target_resp)
        self.env.max_steps = 5

    def evaluate(self, env: CustomerSupportEnv) -> float:
        score = 0.0
        t = env.tickets[0]
        if t.category == "login_issue": score += 0.4
        if t.response and len(t.response) > 5: score += 0.4
        if t.status == "closed": score += 0.2
        return min(max(score, 0.0), 1.0)

class MediumTask(BaseTask):
    def __init__(self):
        tickets = [
            Ticket(id="T1", message="Where is my refund?"),
            Ticket(id="T2", message="How to update billing address?")
        ]
        target_cat = {"T1": "billing", "T2": "account"}
        target_resp = {"T1": "processed 3-5 days", "T2": "settings page"}
        self.env = CustomerSupportEnv(tickets, target_cat, target_resp)
        self.env.max_steps = 10

    def evaluate(self, env: CustomerSupportEnv) -> float:
        score = 0.0
        for t in env.tickets:
            t_score = 0
            if t.id == "T1" and t.category == "billing": t_score += 0.2
            if t.id == "T2" and t.category == "account": t_score += 0.2
            if t.response and len(t.response) > 5: t_score += 0.2
            if t.status == "closed": t_score += 0.1
            score += t_score
        return min(max(score, 0.0), 1.0)

class HardTask(BaseTask):
    def __init__(self):
        tickets = [
            Ticket(id="T1", message="App keeps crashing on startup since update."),
            Ticket(id="T2", message="I was double charged for my subscription."),
            Ticket(id="T3", message="Do you offer enterprise plans?")
        ]
        target_cat = {"T1": "technical", "T2": "billing", "T3": "sales"}
        target_resp = {"T1": "cache", "T2": "refund", "T3": "contact sales"}
        self.env = CustomerSupportEnv(tickets, target_cat, target_resp)
        self.env.max_steps = 15

    def evaluate(self, env: CustomerSupportEnv) -> float:
        score = 0.0
        for t in env.tickets:
            t_score = 0
            if getattr(t, 'category', None) in ["technical", "billing", "sales"]: t_score += 0.15
            if getattr(t, 'response', None) and len(t.response) > 7: t_score += 0.1
            if getattr(t, 'status', None) == "closed": t_score += 0.08
            score += t_score
        return min(max(score, 0.0), 1.0)
