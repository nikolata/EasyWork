from database import Base, engine
import candidates.model
import companies.model
import jobs.model
import messages.model
from jobs.model import JobModel
from database import session_scope
from index_view import CompanyCaller

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # job = JobModel(category_id=1,
    #                title='Dira Miqchka', city='Sofia', position='Miqch', description='da mie qko', company_id=1)
    # session.add(job)
    # session.commit()
    company = CompanyCaller()
    # company.call_sign_up()
    # # call_log_in()
    # company.call_update_profile()
    # company.call_show_all_categories()
    company.call_log_in()
    # company.call_update_job()
    # company.call_show_all_jobs()
    # company.call_delete_job()