from .gateway import MessageGateway


class MessageController:
    def __init__(self):
        self.gateway = MessageGateway()

    def get_all_messages_with_given_company_and_candidate(self, company_id, candidate_id):
        self.gateway.select_messages(company_id, candidate_id)
        self.make_message_seen()

    def add_new_message(self, company_id, candidate_id, send_by, message):
        self.gateway.add_message(company_id, candidate_id, send_by, message)

    def make_message_seen(self):
        self.gateway.update_seen()
