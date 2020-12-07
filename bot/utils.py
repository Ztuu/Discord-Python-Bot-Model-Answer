def get_channel_by_name(client, guild, name):
    """Returns a channel by name from a specific guild"""
    for server in client.guilds:
        if server == guild:
            for channel in server.text_channels:
                if channel.name == name:
                    return channel
