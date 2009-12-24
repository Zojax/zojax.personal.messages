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
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.messaging.interfaces import IMessage, IMessageService, IMessageStorage

_ = MessageFactory('zojax.personal.messages')

SERVICE_ID = u'zojax.personal.messages'


class IPersonalMessage(IMessage):

    title = schema.TextLine(
        title = _(u'Subject'),
        default = u'',
        required = True)

    text = schema.Text(
        title = u'Cooked',
        required = True)

    sender = schema.TextLine(
        title = u'Sender',
        required = True)

    replyto = schema.TextLine(
        title = u'Reply to',
        required = True)


class IPersonalMessageService(IMessageService):
    """ """


class IPersonalMessages(interface.Interface):

    allow_messaging = schema.Bool(
        title = _(u'Allow'),
        description = _(u'Allow other members send message to me.'),
        default = True,
        required = True)


class IMessagesWorkspace(IMessageStorage, IWorkspace):
    """ messages workspace """


class IMessagesWorkspaceFactory(IWorkspaceFactory):
    """ messages workspace factory """
