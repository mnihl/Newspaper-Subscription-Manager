


class Subscriber:
    def __init__(self, subscriber_id, name, address):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.newspapers = []
        self.received = []
        self.received_history = []

    def subscribe(self, newspaper):
        self.newspapers.append(newspaper)
        newspaper.subscribers += 1
    
    def receive_issue(self, issue):
        self.received.append(issue)
        self.received_history.append({
            "issue_id": issue.issue_id,
            "editor": issue.editor.name
        })
        issue.delivered = True
        print(f"Subscriber {self.name} received issue {issue.issue_id} from {issue.editor.name} of {issue.editor.newspapers[0].name}.")

    def stats(self):
        return {
            "name": self.name,
            "address": self.address,
            "subscriptions": [newspaper.name for newspaper in self.newspapers],
            "received": [issue.issue_id for issue in self.received],
        }
    
    def check_undelivered(self):
        return [issue.issue_id for issue in self.received if not issue.delivered]