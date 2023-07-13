from unittest.mock import AsyncMock, Mock, patch

import pytest

from discord.ext import commands
from Discord.main import on_voice_state_update


@pytest.mark.asyncio
@patch("Discord.helpers.on_mute_log")
@patch.object(commands.Bot, "get_channel")
async def test_on_voice_state_update_after_not_muted(mocked_client, mocked_on_mute_log):
    mocked_member, mocked_after, mocked_before = Mock(), Mock(), Mock()
    mocked_before.self_mute = False
    mocked_after.self_mute = True
    mocked_client().send = AsyncMock()

    await on_voice_state_update(mocked_member, mocked_before, mocked_after)

    mocked_client().send.assert_called_once_with(embed=mocked_on_mute_log(mocked_member))


@pytest.mark.asyncio
@patch("Discord.helpers.on_unmute_log")
@patch.object(commands.Bot, "get_channel")
async def test_on_voice_state_update_after_muted(mocked_client, mocked_on_unmute_log):
    mocked_member, mocked_after, mocked_before = Mock(), Mock(), Mock()
    mocked_before.self_mute = True
    mocked_after.self_mute = False
    mocked_client().send = AsyncMock()

    await on_voice_state_update(mocked_member, mocked_before, mocked_after)

    mocked_client().send.assert_called_once_with(embed=mocked_on_unmute_log(mocked_member))
