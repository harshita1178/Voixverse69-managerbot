"""
MIT License

Copyright (c) 2022 Aʙɪsʜɴᴏɪ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import threading
import typing

from sqlalchemy import BigInteger, Boolean, Column, String, distinct, func

# BASE aur SESSION ke saath ENGINE ko bhi import karo
from Database.sql import BASE, SESSION, ENGINE # <-- Ye line change hui hai


class GroupLogs(BASE):
    __tablename__ = "log_channels"
    chat_id = Column(String(14), primary_key=True)
    log_channel = Column(String(14), nullable=False)

    def __init__(self, chat_id, log_channel):
        self.chat_id = str(chat_id)
        self.log_channel = str(log_channel)


class LogChannelSettings(BASE):
    __tablename__ = "log_channel_setting"
    chat_id = Column(BigInteger, primary_key=True)
    log_joins = Column(Boolean, default=True)
    log_leave = Column(Boolean, default=True)
    log_warn = Column(Boolean, default=True)
    log_action = Column(Boolean, default=True)
    # log_media = Column(Boolean)
    log_report = Column(Boolean, default=True)

    def __init__(
        self,
        chat_id: int,
        log_join: bool,
        log_leave: bool,
        log_warn: bool,
        log_action: bool,
        log_report: bool,
    ):
        self.chat_id = chat_id
        self.log_warn = log_warn
        self.log_joins = log_join
        self.log_leave = log_leave
        self.log_report = log_report
        self.log_action = log_action

    def toggle_warn(self) -> bool:
        self.log_warn = not self.log_warn
        SESSION.commit()
        return self.log_warn

    def toggle_joins(self) -> bool:
        self.log_joins = not self.log_joins
        SESSION.commit()
        return self.log_joins

    def toggle_leave(self) -> bool:
        self.log_leave = not self.log_leave
        SESSION.commit()
        return self.log_leave

    def toggle_report(self) -> bool:
        self.log_report = not self.log_report
        SESSION.commit()
        return self.log_report

    def toggle_action(self) -> bool:
        self.log_action = not self.log_action
        SESSION.commit()
        return self.log_action


# Yahan 'bind=ENGINE' add kiya gaya hai
GroupLogs.__table__.create(bind=ENGINE, checkfirst=True) # <-- Ye line change hui hai
LogChannelSettings.__table__.create(bind=ENGINE, checkfirst=True) # <-- Ye line change hui hai

LOGS_INSERTION_LOCK = threading.RLock()
LOG_SETTING_LOCK = threading.RLock()
CHANNELS = {}


def get_chat_setting(chat_id: int) -> typing.Optional[LogChannelSettings]:
    with LOG_SETTING_LOCK:
        return SESSION.query(LogChannelSettings).get(chat_id)


def set_chat_setting(setting: LogChannelSettings):
    with LOGS_INSERTION_LOCK:
        res: LogChannelSettings = SESSION.query(LogChannelSettings).get(setting.chat_id)
        if res:
            res.log_warn = setting.log_warn
            res.log_action = setting.log_action
            res.log_report = setting.log_report
            res.log_joins = setting.log_joins
            res.log_leave = setting.log_leave
        else:
            SESSION.add(setting)
    SESSION.commit()


def set_chat_log_channel(chat_id, log_channel):
    with LOGS_INSERTION_LOCK:
        res = SESSION.query(GroupLogs).get(str(chat_id))
        if res:
            res.log_channel = log_channel
        else:
            res = GroupLogs(chat_id, log_channel)
            SESSION.add(res)

        CHANNELS[str(chat_id)] = log_channel
        SESSION.commit()


def get_chat_log_channel(chat_id):
    return CHANNELS.get(str(chat_id))


def stop_chat_logging(chat_id):
    with LOGS_INSERTION_LOCK:
        res = SESSION.query(GroupLogs).get(str(chat_id))
        if res:
            if str(chat_id) in CHANNELS:
                del CHANNELS[str(chat_id)]

            log_channel = res.log_channel
            SESSION.delete(res)
            SESSION.commit()
            return log_channel


def num_logchannels():
    try:
        return SESSION.query(func.count(distinct(GroupLogs.chat_id))).scalar()
    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with LOGS_INSERTION_LOCK:
        chat = SESSION.query(GroupLogs).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
            SESSION.add(chat)
            if str(old_chat_id) in CHANNELS:
                CHANNELS[str(new_chat_id)] = CHANNELS.get(str(old_chat_id))

        SESSION.commit()


def __load_log_channels():
    global CHANNELS
    try:
        all_chats = SESSION.query(GroupLogs).all()
        CHANNELS = {chat.chat_id: chat.log_channel for chat in all_chats}
    finally:
        SESSION.close()


__load_log_channels()
