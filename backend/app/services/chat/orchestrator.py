from app.services.chat.intent_detector import IntentDetector
from app.services.chat.query_router import QueryRouter
from app.services.chat.context_service import ContextService


class ChatOrchestrator:
    def __init__(self, db):
        self.detector = IntentDetector()
        self.router = QueryRouter()
        self.context_service = ContextService(db)

    def build_context(self, message: str) -> str:
        intent = self.detector.detect(message)
        required = self.router.get_required_context(intent)
        return self.context_service.build_context(required)