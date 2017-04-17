from django.http import Http404
from Store.models import UserProfile, Market, Stuff, Sale


def check_premissions(request, model):
    if model.user_id != request.user.id:
        raise Http404
