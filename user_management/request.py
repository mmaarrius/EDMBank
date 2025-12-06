from datetime import datetime
import uuid

class Request:
    def __init__(self, username: str, email: str, title: str, concern: str, status: str = "Open", timestamp: datetime = None, request_id: str = None):
        self.username = username
        self.email = email
        self.title = title
        self.concern = concern
        self.status = status
        self.timestamp = timestamp if timestamp else datetime.now()
        self.request_id = request_id if request_id else str(uuid.uuid4())

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "username": self.username,
            "email": self.email,
            "title": self.title,
            "concern": self.concern,
            "status": self.status,
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: dict):
        return Request(
            username=data.get("username"),
            email=data.get("email"),
            title=data.get("title"),
            concern=data.get("concern"),
            status=data.get("status", "Open"),
            timestamp=datetime.fromisoformat(data.get("timestamp")) if data.get("timestamp") else None,
            request_id=data.get("request_id")
        )
