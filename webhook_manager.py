__date__ = '29/08/19'
__author__ = 'Rahul K P'

import http.client
import json

from app import db
from models import Webhooks

class WebhookManager:

    def triger_webhook(self, host, method, endpoint, payload):
        """Method to trigger webhook.

        Args:
            host (str): Webhook host name
            method (str): POST / GET
            endpoint (str): End point to send webhook
            payload (str): Payload to send webhook

        """
        conn = http.client.HTTPSConnection(host)
        conn.request(method, endpoint, json.dumps(payload), {'Content-Type': 'application/json'})

    def triger_all_webhooks(self, event, payload):
        """Method to trigger all webhooks related ro a event.

        Args:
            event (str): Name of event
            payload (str): Payload to send webhook
            
        """
        webhooks = Webhooks.query.filter(Webhooks.event == event).all()
        for webhook in webhooks:
            if isinstance(webhook.extra_paylod, str):
                payload.update(json.loads(webhook.extra_paylod))
            payload.update(webhook.extra_paylod)
            self.triger_webhook(webhook.host, webhook.method, webhook.endpoint, payload)

    def create_webhook(self, webhook_dict):
        """Method to create a webhook in database

        Args:
            webhook_dict (dict): Webhook dict info
        
        Returns:
            Returns a dictionary with status and message.
    
        """
        try:
            webhook = Webhooks(host=webhook_dict['host'],
                                endpoint=webhook_dict['endpoint'],
                                method=webhook_dict['method'],
                                event=webhook_dict['event'],
                                extra_paylod=webhook_dict['extra_paylod'])
            db.session.add(webhook)
            db.session.commit()
            db.session.flush()
            return {'status': 'SUCCESS', 'msg': 'Webhook created successfully'}
        except Exception as error:
            return {'status': 'FAILED', 'msg': 'Webhook creation failed.'}
