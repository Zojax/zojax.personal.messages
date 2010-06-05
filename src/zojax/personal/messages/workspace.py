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
from zope import interface, component, event
from zope.component import getAdapter
from zope.i18n import translate
from zope.proxy import removeAllProxies
from zope.security.interfaces import IPrincipal
from zope.security.proxy import removeSecurityProxy
from zope.lifecycleevent import ObjectCreatedEvent, ObjectModifiedEvent
from zope.app.container.contained import Contained

from zojax.catalog.utils import getRequest
from zojax.messaging.storage import MessageStorage
from zojax.messaging.interfaces import IMessageStorage
from zojax.personal.space.interfaces import IPersonalSpace
from zojax.content.space.workspace import WorkspaceFactory

from interfaces import _, IMessagesWorkspace, IMessagesWorkspaceFactory


class MessagesWorkspace(MessageStorage, Contained):
    interface.implements(IMessagesWorkspace)

    title = _('Messages')

    @property
    def space(self):
        return self.__parent__


class MessagesWorkspaceFactory(WorkspaceFactory):
    component.adapts(IPersonalSpace)
    interface.implements(IMessagesWorkspaceFactory)

    name = u'messages'
    description = _(u'Personal messaging service.')
    weight = 1000

    @property
    def title(self):
        if self.isInstalled():
            messages = self.install()
            lmsg = len(messages.messages)
            if lmsg:
                return translate(
                    u'Messages (${number})', 'zojax.personal.messages',
                    mapping={'number': lmsg})

        return _(u'Messages')

    def install(self):
        ws = self.space.get(self.name)

        if not IMessagesWorkspace.providedBy(ws):
            ws = MessagesWorkspace(self.space.principalId)
            event.notify(ObjectCreatedEvent(ws))
            removeAllProxies(self.space)[self.name] = ws
            ws.__name__ = self.name
            ws.__parent__ = removeAllProxies(self.space)

        return ws

    def isAvailable(self):
        request = getRequest()
        if request is not None and request.principal.id != self.space.principalId:
            return False

        return True


@component.adapter(IPrincipal)
@interface.implementer(IMessageStorage)
def getMessageStorage(principal):
    space = IPersonalSpace(principal, None)
    if space is not None:
        return getAdapter(
            space, IMessagesWorkspaceFactory, 'messages').install()
