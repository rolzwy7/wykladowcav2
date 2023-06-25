from django.db.models import CASCADE, ForeignKey, Model


class WebinarApplicationAppliedDiscount(Model):
    application = ForeignKey("WebinarApplication", on_delete=CASCADE)
    # TODO: WebinarApplicationAppliedDiscount
