import pytest

from aioscheduler import AsyncIOScheduler
from aioscheduler.scheduler import work_available


@pytest.fixture
def scheduler(request):
    s = AsyncIOScheduler()
    request.addfinalizer(s.stop)
    return s


@pytest.fixture
def started_scheduler(scheduler):
    scheduler.start()
    return scheduler


@pytest.fixture
def work_available_event():
    return work_available
