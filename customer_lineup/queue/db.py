from customer_lineup.utils.db_models import *
from datetime import datetime

@db_session
def add_queue_element(webuser_ref, workplace_ref, status, type, waiting_person):
    queue = QueueElement(web_users_ref = webuser_ref, workplaces_ref = workplace_ref, status = status, type = type, waiting_person = waiting_person)
    return queue

@db_session
def get_queue_with_id(id):
    queue = QueueElement.get(id=id)
    return queue

@db_session
def get_all_user_queues(user_ref):
    queues = QueueElement.select(lambda q: q.web_users_ref.email_address == user_ref.email_address)
    return queues

@db_session
def get_active_queue(user_ref):
    queue = QueueElement.get(web_users_ref=user_ref, status=1)
    return queue

@db_session
def change_queue_status(queue_id, status):
    queue = get_queue_with_id(queue_id)
    queue.status = status
    queue.status_time = datetime.now()
    return queue

@db_session
def get_users_on_queue_with_workplace(workplace_ref):
    queues = QueueElement.select(lambda q: q.workplaces_ref == workplace_ref and q.status == 1)
    return queues

