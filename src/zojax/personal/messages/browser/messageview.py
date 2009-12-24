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
from email.Utils import formataddr

from zope import interface, schema, component
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.security.interfaces import IAuthentication
from zope.app.security.interfaces import PrincipalLookupError

from zojax.richtext.field import RichText
from zojax.messaging.interfaces import IMessageStorage
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.mailtemplate.interfaces import IMailHeaders, IMailTemplate

from zojax.layoutform import interfaces
from zojax.layoutform import button, Fields, PageletForm
from zojax.personal.messages.interfaces import _, SERVICE_ID, IPersonalMessage


class IMessage(interface.Interface):

    title = schema.TextLine(
        title = _(u'Subject'),
        default = u'',
        required = True)

    body = RichText(
        title = _('Message body'),
        required = True)


class MessageView(PageletForm):

    label = _(u'Reply')
    fields = Fields(IMessage)

    def getContent(self):
        context = self.context
        if not context.title.startswith(u'Re:'):
            return {'title': u'Re: %s'%context.title,
                    'body': u'<blockquote>%s</blockquote><br />'%context.text}
        else:
            return {'title': u'',
                    'body': u'<blockquote>%s</blockquote><br />'%context.text}

    def update(self):
        request = self.request
        context = removeAllProxies(self.context)
        context.__status__ = False

        try:
            sender = getUtility(IAuthentication).getPrincipal(context.sender)
        except PrincipalLookupError:
            sender = None

        self.replyTo = sender
        self.messaging = IMessageStorage(self.replyTo, None)

        if sender is not None:
            profile = IPersonalProfile(sender, None)
            self.sender = getattr(profile, 'title', sender.title)

            space = getattr(profile, 'space', None)
            if space is not None:
                self.profile = '%s/'%absoluteURL(space, request)
            else:
                self.profile = ''
        else:
            self.sender = context.sender
            self.profile = ''

        oldcontext = self.context

        self.context = context
        super(MessageView, self).update()
        self.context = oldcontext

    @button.buttonAndHandler(_(u'Send reply'), provides=interfaces.IAddButton)
    def handleReply(self, action):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
        else:
            data['text'] = data['body'].cooked
            data['sender'] = unicode(
                self.context.__parent__.__parent__.principalId)
            data['replyto'] = unicode(self.context.__uid__)

            self.messaging.create(SERVICE_ID, **data)

            IStatusMessage(self.request).add(_(u'Message has been sent.'))
            self.redirect('../')


class MessageMail(object):

    def update(self):
        request = self.request
        context = removeAllProxies(self.context)

        try:
            sender = getUtility(IAuthentication).getPrincipal(context.sender)
        except PrincipalLookupError:
            sender = None

        self.replyTo = sender
        self.messaging = IMessageStorage(self.replyTo, None)

        if sender is not None:
            profile = IPersonalProfile(sender, None)
            self.sender = getattr(profile, 'title', sender.title)

            space = getattr(profile, 'space', None)
            if space is not None:
                self.profile = '%s/'%absoluteURL(space, request)
            else:
                self.profile = ''
        else:
            self.sender = context.sender
            self.profile = ''

        self.context = context


class FromAddress(object):
    interface.implements(IMailHeaders)
    component.adapts(IMailTemplate, IPersonalMessage)

    headers = ()

    def __init__(self, template, context):
        try:
            sender = getUtility(IAuthentication).getPrincipal(context.sender)
        except PrincipalLookupError:
            sender = None

        if sender is not None:
            profile = IPersonalProfile(sender, None)
            if profile is not None and profile.email:
                title = u'%s %s'%(profile.firstname, profile.lastname)

                self.headers = (
                    ('From', formataddr((title.strip(), profile.email)), True),)
