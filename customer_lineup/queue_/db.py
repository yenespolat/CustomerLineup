from customer_lineup.utils.db_models import *
from datetime import datetime
from pony.orm import desc


@db_session
def add_queue_element(webuser_ref, workplace_ref, status, type, waiting_person):
    queue = QueueElement(web_users_ref=webuser_ref, workplaces_ref=workplace_ref, status=status, type=type,
                         waiting_person=waiting_person)
    return queue


@db_session
def get_queue_with_id(id):
    queue = QueueElement.get(id=id)
    return queue


@db_session
def get_all_user_queues(user_ref):
    queues = QueueElement.select(lambda q: q.web_users_ref.email_address == user_ref.email_address).order_by(lambda qe: desc(qe.taking_time))
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


@db_session
def get_all_q_today(wp_id):
    queues = QueueElement.select(lambda q: q.workplaces_ref.id == wp_id and q.status_time.day == datetime.now().day and
                                 q.status_time.month == datetime.now().month and q.status_time.year == datetime.now().year)
    return queues


@db_session
def get_all_q(wp_id):
    queues = QueueElement.select(lambda q: q.workplaces_ref.id == wp_id)
    return queues


def get_queue_element(**kwargs) -> QueueElement:
    return QueueElement.get(**kwargs)
