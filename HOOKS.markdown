# Available Hooks

## Boring ones...
* **MADE_CONNECTION**

  When connection is made to the IRC server

  Arguments:

* **LOST_CONNECTION**

  When connection is lost to the IRC server.

  Arguments: reason

* **SIGNED_ON**

  When the bot signs into IRC.

  Arguments:

* **JOINED**

  When the bot has joined a channel.

  Arguments: channel

* **LEFT**

  When the bot has left a channel.

  Arguments: channel

## Exciting ones...
* **ATME**

  On reception of a non-whisper message directed at the bot.

  Arguments: username, channel, message

* **MESSAGE**

  On reception of a non-whisper message.

  Arguments: username, channel, message

* **WHISPER**

  On reception of a whisper message.

  Arguments: username, message

* **ACTION**

  On reception of a user action.

  Arguments: username, channel, message

* **NICK_CHANGE**

  When a user changes nicks.

  Arguments: old_nick, new_nick