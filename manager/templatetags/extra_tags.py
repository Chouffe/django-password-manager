from django import template
from manager.models import CryptoEngine

register = template.Library()

@register.filter(is_safe=True)
def decrypt(text, master_key):
    engine = CryptoEngine(master_key=master_key)
    return engine.decrypt(text)
