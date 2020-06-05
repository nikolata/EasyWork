from .gateway import MessageGateway


class MessageController:
    def __init__(self):
        self.gateway = MessageGateway()

    def get_all_messages_with_given_company_and_candidate(self, company_id, candidate_id):
        messages = self.gateway.select_messages(company_id, candidate_id)
        self.make_message_seen(company_id, candidate_id)
        return messages

    def add_message(self, company_id, candidate_id, send_by, message):
        self.gateway.add_message(company_id, candidate_id, send_by, message)

    def make_message_seen(self, company_id, candidate_id):
        self.gateway.update_seen(company_id, candidate_id)

    def get_all_companies_a_candidate_messaged(self, candidate_id):
        return self.gateway.select_company_id(candidate_id)

    def get_messages(self, company_id, candidate_id):
        return self.gateway.select_messages(company_id, candidate_id)
