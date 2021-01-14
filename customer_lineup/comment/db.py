from customer_lineup.utils.db_models import *

@db_session
def add_comment_wo_qelement(webuser_ref, workplace_ref, score, comment):
    comment = Comment(web_user_ref=webuser_ref, workplace_ref=workplace_ref, score=score, comment=comment)
    return comment

@db_session
def add_comment_with_qelement(webuser_ref, workplace_ref, score, comment, queue_ref):
    comment = Comment(web_user_ref=webuser_ref, workplace_ref=workplace_ref, score=score, comment=comment, queue_element_ref=queue_ref)
    return comment

@db_session
def assign_qelement_to_comment(comment_ref, queue_ref):
    comment_ref.queue_element_ref = queue_ref
    return

@db_session
def get_comment(id):
    comment = Comment.get(id=id)
    return comment

@db_session
def delete_comment(id):
    return Comment.get(id=id).delete()