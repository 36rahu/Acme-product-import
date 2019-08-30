__date__ = '29/08/19'
__author__ = 'Rahul K P'

import http.client
import json

from app import db
from models import Webhooks

class WebhookManager:

	def triger_webhook(self, host, method, endpoint, payload):
		print(endpoint)
		conn = http.client.HTTPSConnection(host)
		conn.request(method, endpoint, json.dumps(payload), {'Content-Type': 'application/json'})

	def triger_all_webhooks(self, event, payload):
		webhooks = Webhooks.query.filter(Webhooks.event == event).all()
		for webhook in webhooks:
			if isinstance(webhook.extra_paylod, str):
				payload.update(json.loads(webhook.extra_paylod))
			payload.update(webhook.extra_paylod)
			self.triger_webhook(webhook.host, webhook.method, webhook.endpoint, payload)

	def create_webhook(self, webhook_dict):
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
