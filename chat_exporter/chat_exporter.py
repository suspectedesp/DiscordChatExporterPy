import datetime
import io
from typing import List, Optional

from chat_exporter.construct.transcript import Transcript
from chat_exporter.ext.discord_import import discord
from chat_exporter.construct.attachment_handler import (
    AttachmentHandler,
    AttachmentToLocalFileHostHandler,
    AttachmentToDiscordChannelHandler,
)


async def quick_export(
    channel: discord.TextChannel,
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
) -> Optional[discord.Message]:
    """
    Create a Quick Transcript of your Discord channel.

    Parameters
    ----------
    channel: :class:`discord.TextChannel`
        The Channel to Export
    guild: Optional[:class:`discord.Guild`]
        The Guild to Export
    bot: Optional[:class:`discord.Client`]
        The Bot to use for getting member role colour

    Returns
    -------
    Optional[:class:`discord.Message`]
        The Sent Message
    """

    if guild:
        channel.guild = guild

    transcript = (
        await Transcript(
            channel=channel,
            limit=None,
            messages=None,
            pytz_timezone="UTC",
            military_time=True,
            fancy_times=True,
            before=None,
            after=None,
            support_dev=True,
            bot=bot,
            attachment_handler=None,
        ).export()
    ).html

    if not transcript:
        return

    transcript_embed = discord.Embed(
        description=f"**Transcript Name:** transcript-{channel.name}\n\n",
        colour=discord.Colour.blurple(),
    )

    transcript_file = discord.File(
        io.BytesIO(transcript.encode()), filename=f"transcript-{channel.name}.html"
    )
    return await channel.send(embed=transcript_embed, file=transcript_file)


async def export(
    channel: discord.TextChannel,
    limit: Optional[int] = None,
    tz_info="UTC",
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    military_time: Optional[bool] = True,
    fancy_times: Optional[bool] = True,
    before: Optional[datetime.datetime] = None,
    after: Optional[datetime.datetime] = None,
    support_dev: Optional[bool] = True,
    attachment_handler: Optional[AttachmentHandler] = None,
) -> str:
    """
    Create a Customised Transcript of your Discord channel.

    Parameters
    ----------
    channel: :class:`discord.TextChannel`
        The Channel to Export
    limit: Optional[:class:`int`]
        The Limit of Messages to Export
    tz_info: Optional[:class:`str`]
        The Timezone of the Transcript
    guild: Optional[:class:`discord.Guild`]
        The Guild to Export
    bot: Optional[:class:`discord.Client`]
        The Bot to Use for Fetching Data
    military_time: Optional[:class:`bool`]
        Whether to Use Military Time (24 Hour Clock)
    fancy_times: Optional[:class:`bool`]
        Whether to Use Fancy Times (JavaScript)
    before: Optional[:class:`datetime.datetime`]
        The Date to Fetch Messages Before
    after: Optional[:class:`datetime.datetime`]
        The Date to Fetch Messages After
    attachment_handler: Optional[:class:`AttachmentHandler`]
        The Attachment Handler to Use

    Returns
    -------
    :class:`str`
        The HTML of the Transcript
    """

    if guild:
        channel.guild = guild

    return (
        await Transcript(
            channel=channel,
            limit=limit,
            messages=None,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=before,
            after=after,
            support_dev=support_dev,
            bot=bot,
            attachment_handler=attachment_handler,
        ).export()
    ).html


async def raw_export(
    channel: discord.TextChannel,
    messages: List[discord.Message],
    tz_info="UTC",
    guild: Optional[discord.Guild] = None,
    bot: Optional[discord.Client] = None,
    military_time: Optional[bool] = False,
    fancy_times: Optional[bool] = True,
    support_dev: Optional[bool] = True,
    attachment_handler: Optional[AttachmentHandler] = None,
) -> str:
    """
    Create a Customised Transcript of your Discord channel with Raw Messages.

    Parameters
    ----------
    channel: :class:`discord.TextChannel`
        The Channel to Export
    messages: List[:class:`discord.Message`]
        The Messages to Export
    tz_info: Optional[:class:`str`]
        The Timezone of the Transcript
    guild: Optional[:class:`discord.Guild`]
        The Guild to Export
    bot: Optional[:class:`discord.Client`]
        The Bot to Use for Fetching Data
    military_time: Optional[:class:`bool`]
        Whether to Use Military Time (24 Hour Clock)
    fancy_times: Optional[:class:`bool`]
        Whether to Use Fancy Times (JavaScript)
    attachment_handler: Optional[:class:`AttachmentHandler`]
        The Attachment Handler to Use

    Returns
    -------
    :class:`str`
        The HTML of the Transcript
    """

    if guild:
        channel.guild = guild

    return (
        await Transcript(
            channel=channel,
            limit=None,
            messages=messages,
            pytz_timezone=tz_info,
            military_time=military_time,
            fancy_times=fancy_times,
            before=None,
            after=None,
            support_dev=support_dev,
            bot=bot,
            attachment_handler=attachment_handler,
        ).export()
    ).html


async def quick_link(
    channel: discord.TextChannel, guild: Optional[discord.Guild] = None
) -> Optional[discord.Message]:
    """
    Return a Message with a Link to the Transcript of the Channel.

    Parameters
    ----------
    channel: :class:`discord.TextChannel`
        The Channel to Send the Link
    message: :class:`discord.Message`
        The Message to Export

    Returns
    -------
    :class:`discord.Message`
        The Sent Message
    """

    embed = discord.Embed(
        title="Transcript Link",
        description=(
            f"[Click here to view the transcript](https://mahto.id/chat-exporter?url={message.attachments[0].url})"
        ),
        colour=discord.Colour.blurple(),
    )

    return await channel.send(embed=embed)


async def link(message: discord.Message) -> str:
    """
    Return a Viewable Link to the Transcript of the Message.

    Parameters
    ----------
    message: :class:`discord.Message`
        The Message to Export

    Returns
    -------
    :class:`str`
        The Link to the Transcript
    """

    return "https://mahto.id/chat-exporter?url=" + message.attachments[0].url
