from database import Base, engine
import candidates.model
import companies.model
import jobs.model
import messages.model
from jobs.model import JobModel
from database import session

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    job = JobModel(category_id=1,
                   title='Dira Miqchka', city='Sofia', position='Miqch', description='da mie qko', company_id=1)
    session.add(job)
    session.commit()
