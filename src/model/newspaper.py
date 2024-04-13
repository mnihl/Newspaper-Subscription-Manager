from typing import List
from flask_restx import Model
from .issue import Issue
from .editor import Editor
# from .agency import Agency
from .subscriber import Subscriber
import datetime
import random
import uuid


class Newspaper(object):
    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.subscribers = 0
        self.issues: List[Issue] = []

    def list_all_issues(self, paper_id):
        if self.paper_id == paper_id:
            return self.issues
    
    def create_new_issue(self):
        issue_id = uuid.uuid4().int % 1000
        self.issues.append(Issue(datetime.datetime.now(), random.randint(10, 20), issue_id))
    
    def get_issue(self, issue_id):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None
    
    def update(self, paper_id, name = None, frequency = None, price = None):
        if name is not None:
            self.name = name
        if frequency is not None:
            self.frequency = frequency
        if price is not None:
            self.price = price

    def release_issue(self, issue_id):
        issue = self.get_issue(issue_id)
        if issue:
            issue.publish()
            return True
        return False

    
    def stats(self):
        return {
            "name": self.name,
            "subscribers": self.subscribers,
            "monthly revenue": self.subscribers * self.price,
            "annual revenue": (self.subscribers * self.price) * 12,
        }