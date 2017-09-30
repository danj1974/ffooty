from django.apps import AppConfig


class FfootyConfig(AppConfig):
    name = 'ffooty'
    verbose_name = "Fantasy Football"

    # def ready(self):
    #     print "READY"
    #     from signals import *