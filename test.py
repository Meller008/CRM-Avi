from classes.repository import WorkerRepository
from classes.pony_models import Staff_worker_info
from datetime import datetime
from classes.worker import Worker
from pony.orm import db_session, select, left_join
from collections import namedtuple

# worker = WorkerMapper().find(5)
# print(worker.first_name, worker.last_name)

# workers = WorkerMapper().list()
# #print(workers)
