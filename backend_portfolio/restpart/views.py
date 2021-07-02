from backend_portfolio.userpart.models import TypeFeedBack
from .serializers import *
from rest_framework.generics import *
from userpart.models import *

class FeedBackView(ListAPIView):
    serializer_class = FeedBackSerializer
    queryset = Feedback.objects.all()
    lookup_field = "type_feedback"

    def get_queryset(self):
        type_feedback = self.kwargs["type_feedback"]
        return Feedback.objects.filter(type_feedback=type_feedback)


class TypeFeedBackView(ListCreateAPIView):
    serializer_class = TypeFeedBackSerializer
    queryset = TypeFeedBackSerializer.objects.all()