import logging
from .backend_client import BackendClient
from .events_client import EventsClient
from dotenv import load_dotenv
import os

load_dotenv()

log = logging.getLogger(__name__)


class EventPoller:
    def __init__(self):
        self.log = log
        self.log.info('Initializing event poller')
        self.events_api_url = os.getenv('API_BASE_URL')
        self.backend_api_url = os.getenv('BACKEND_API_BASE_URL')
        self.events_client = EventsClient(self.events_api_url)
        self.backend_client = BackendClient(self.backend_api_url)
        self.log.info('Event poller initialized')

    def format_event_data(self, event: dict):
        formatted_event = {
            'base_event_id': event.get('base_event_id'),
            'event_id': event.get('event_id'),
            'title': event.get('title'),
            'start_date_time': event.get('event_start_date'),
            'end_date_time': event.get('event_end_date'),
            'min_price': min(event.get('prices'), default=0),
            'max_price': max(event.get('prices'), default=0),
        }
        return formatted_event

    def submit_event(self, event_data: dict):
        formatted_event = self.format_event_data(event_data)
        return self.backend_client.add_event(formatted_event)

    def get_unprocessed_events(self, events):
        unprocessed_events_list = []
        processed_event_ids = self.backend_client.get_processed_event_ids()
        for event in events:
            base_event_id = event.get('base_event_id')
            event_id = event.get('event_id')
            unique_event_id = f"{base_event_id}:{event_id}"
            if unique_event_id not in processed_event_ids:
                unprocessed_events_list.append(event)
                self.log.info(f"Found unprocessed event: {unique_event_id}")
            else:
                self.log.info(f'Event {unique_event_id} is already processed.')
        return unprocessed_events_list

    def poll_events(self):
        try:
            events = self.events_client.get_events()
            unprocessed_events = self.get_unprocessed_events(events=events)
            processed_event_count = 0
            for event in unprocessed_events:
                if event.get('sell_mode') == 'online':
                    self.submit_event(event_data=event)
                    processed_event_count += 1
                else:
                    base_event_id = event.get('base_event_id')
                    event_id = event.get('event_id')
                    self.log.info(
                        f'Ignoring offline event with base event id {base_event_id} and event id {event_id}'
                    )

            self.log.info(f'Processed {processed_event_count} events')
        except Exception as err:
            self.log.error(f'Error polling events: {err}')
