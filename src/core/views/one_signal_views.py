from django.http import HttpResponse


def one_signal_worker_script(request):
    """One signal worker script"""
    content = (
        "importScripts('https://cdn.onesignal.com/sdks/OneSignalSDKWorker.js');"
    )
    return HttpResponse(
        content.encode("utf8"), content_type="application/javascript"
    )
