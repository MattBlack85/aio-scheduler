from tenacity import retry, stop_after_attempt, wait_fixed


def test_after_start_no_work_available(started_scheduler, work_available_event):
    """
    We have called .start on the thread, assure that the Event is set to False
    """
    assert work_available_event.is_set() is False


def test_after_start_event_loop_not_running(started_scheduler):
    """
    We have called .start on the thread, assure that the Event is set to False
    """
    assert started_scheduler.loop.is_running() is False


@retry(stop=stop_after_attempt(5), wait=wait_fixed(0.1))
def test_adding_periodic_task_starts_event_loop(started_scheduler, dummy_coroutine):
    """
    Ensure that after calling .add_periodic the scheduler event loop starts running
    """
    started_scheduler.add_periodic('name', dummy_coroutine, 1, started_scheduler.loop)
    assert started_scheduler.loop.is_running()


def test_adding_periodic_task_work_available(started_scheduler, dummy_coroutine,
                                             work_available_event):
    """
    Ensure that after calling .add_periodic the work_available Event is set to True
    """
    started_scheduler.add_periodic('name', dummy_coroutine, 1, started_scheduler.loop)
    assert work_available_event.is_set()
