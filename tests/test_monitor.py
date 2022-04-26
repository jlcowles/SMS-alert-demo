from analogassesment.monitor import Monitor

def test_update_data():
    monitor = Monitor()

    monitor.update_data({'success': True, 'delay':1})
    assert monitor._Monitor__total_messages == 1
    assert monitor._Monitor__failed_messages == 0
    assert monitor._Monitor__average == 1

    monitor.update_data({'success': False, 'delay':0})
    assert monitor._Monitor__total_messages == 2
    assert monitor._Monitor__failed_messages == 1
    assert monitor._Monitor__average == .5

    monitor.update_data({'success': False, 'delay':5})
    assert monitor._Monitor__total_messages == 3
    assert monitor._Monitor__failed_messages == 2
    assert monitor._Monitor__average == 2
