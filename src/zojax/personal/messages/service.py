##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zojax.messaging.service import MessageService

from message import PersonalMessage
from interfaces import _, IPersonalMessageService


class PersonalMessages(MessageService):
    interface.implements(IPersonalMessageService)

    title = _(u'Personal messages')
    description = u''
    priority = 9999

    def create(self, **data):
        message = PersonalMessage(data.get('title',u''))
        message.text = data.get('text',u'')
        message.sender = data.get('sender',u'')
        message.replyTo = data.get('replyTo',u'')
        return message
