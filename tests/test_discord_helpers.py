from unittest.mock import Mock, patch


from Discord.helpers import leave_log

@patch("Discord.helpers.kyiv_time")
def test_leave_log(mocked_kyiv_time):
    mocked_member = Mock()
    mocked_member.name = "test_name"
    mocked_time = "kek"
    mocked_kyiv_time.return_value = mocked_time

    embed = leave_log(mocked_member)

    assert embed.title == f'{mocked_member.name} left channel at {mocked_time}'
    mocked_kyiv_time.assert_called_once()


