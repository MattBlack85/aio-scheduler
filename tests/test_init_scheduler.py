def test_after_start_no_work_available(started_scheduler, work_available_event):
    """
    We have called .start on the thread, assure that the Event is set to False
    """
    assert work_available_event.is_set() is False
