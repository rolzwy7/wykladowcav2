# celery_send_certain_online_email
# celery_send_canceled_email
# celery_send_opinion_email
# celery_send_certificate_email
# celery_send_seminar_invoice_to_ingksiegowosc
# celery_send_subscription_invoice_to_infakt
# celery_subscription_link_to_email
# celery_subscription_pending_transaction
# celery_participant_application_notification_email
# celery_application_confirmation_email
# celery_send_opinion_reward_url_to_email


# class BaseTaskWithRetry(celery.Task):
#     autoretry_for = (Exception,)
#     retry_kwargs = {"max_retries": 10}
#     retry_backoff = 5  # 5 seconds
#     retry_backoff_max = 600  # 1 minute
#     retry_jitter = True
