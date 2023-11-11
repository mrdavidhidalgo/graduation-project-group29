from typing import Optional
from .db_model import db_model as models

from services.test.contracts import test_repository
from typing import List
from sqlalchemy.orm import Session

from services.test.model import test_model

class DBTestRepository(test_repository.TestRepository):
    
    def __init__(self, db: Session) -> None:
        super().__init__()
        self.db = db
        
    def get_by_name(self, name: str)-> Optional[test_model.Test]:
        test = self.db.query(models.Test).filter(models.Test.name == name).first() 
        return None if test is None else test_model.Test(    
                                                         name = test.name,
                                                         technology = test.technology,
                                                         duration_minutes = test.duration_minutes,
                                                         status = test.status.name,
                                                         start_date = test.start_date,
                                                         end_date = test.end_date,
                                                         description = test.description)
        
    def save(self, test: test_model.Test)-> None:
        new_test = models.Test(**test.dict())
        
        self.db.add(new_test)
        self.db.commit()

    def get_tests(self)-> List[test_model.Test]:
        tests = self.db.query(models.Test).all() 
        return [] if tests is None else [test_model.Test(       name = test.name,
                                                                technology = test.technology,
                                                                duration_minutes = test.duration_minutes,
                                                                status = test.status.name,
                                                                start_date = test.start_date,
                                                                end_date = test.end_date,
                                                                description = test.description) for test in tests]



    def save_results(self, results: List[test_model.TestResult])-> None:
        new_results  = [models.TestResult(**rest.dict()) for rest in results]
        
        for new_result in new_results:
            self.db.merge(new_result)
        self.db.commit()