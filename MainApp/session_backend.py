from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from .models import ProductInBasket

class SessionStore(DbSessionStore):
    def cycle_key(self):
        old_session_key = super(SessionStore, self).session_key
        super(SessionStore, self).cycle_key()
        self.save()
        ProductInBasket.objects.filter(session_key=old_session_key).update(session_key=self.session_key)