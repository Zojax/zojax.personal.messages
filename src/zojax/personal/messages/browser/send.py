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
from zope import interface, schema
from zope.publisher.interfaces import NotFound
from zope.app.security.interfaces import IUnauthenticatedPrincipal

from zojax.layoutform import interfaces
from zojax.layoutform import button, Fields, PageletForm
from zojax.richtext.field import RichText
from zojax.messaging.interfaces import IMessageStorage
from zojax.preferences.interfaces import IPreferenceGroup
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.personal.messages.interfaces import _, SERVICE_ID, IPersonalMessages


class IMessage(interface.Interface):

    title = schema.TextLine(
        title = _(u'Subject'),
        default = u'',
        required = True)

    body = RichText(
        title = _('Message body'),
        required = True)


class SendMessage(PageletForm):

    fields = Fields(IMessage)
    ignoreContext = True

    @property
    def label(self):
        return _(u'Send private message to ${user}',
                 mapping={'user': self.context.__principal__.title})

    @button.buttonAndHandler(_(u'Send'), provides=interfaces.IAddButton)
    def handleSend(self, action):
        request = self.request
        data, errors = self.extractData()

        if errors:
            IStatusMessage(request).add(self.formErrorsMessage, 'error')
        else:
            data['text'] = data['body'].cooked
            data['sender'] = unicode(request.principal.id)

            messaging = IMessageStorage(self.context.__principal__)
            messaging.create(SERVICE_ID, **data)

            IStatusMessage(self.request).add(_(u'Message has been sent.'))

            self._finishedAdd = True
            self.redirect('.')

    @button.buttonAndHandler(_(u'Cancel'), provides=interfaces.ICancelButton)
    def handleCancel(self, action):
        self.redirect('.')

    def render(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            prefs = IPersonalMessages(self.context.__principal__)

            if prefs.allow_messaging:
                return super(SendMessage, self).render()

        raise NotFound(self, self.__name__, self.request)
