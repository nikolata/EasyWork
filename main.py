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
