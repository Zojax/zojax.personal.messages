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
from zope import interface, component
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zojax.content.actions.action import Action
from zojax.content.actions.interfaces import IAction
from zojax.messaging.interfaces import IMessageStorage
from zojax.personal.profile.interfaces import IProfileWorkspace
from zojax.personal.messages.interfaces import _, IPersonalMessages


class ISendPrivateMessage(IAction):
    pass


class SendPrivateMessage(Action):
    interface.implements(ISendPrivateMessage)
    component.adapts(IProfileWorkspace, interface.Interface)

    title = _('Send private message')
    weight = 99999

    @property
    def url(self):
        return '%s/sendmessage.html'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return False

        principal = self.context.__principal__

        if self.request.principal.id == principal.id:
            return False

        messaging = IMessageStorage(principal, None)
        if messaging is None:
            return False

        return IPersonalMessages(principal).allow_messaging
