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
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError
from zojax.principal.profile.interfaces import IPersonalProfile


class ServiceView(object):

    def listMessages(self):
        service = self.context
        request = self.request
        getPrincipal = getUtility(IAuthentication).getPrincipal

        for msgId in service:
            message = service.get(msgId)

            try:
                sender = getPrincipal(message.sender)
            except PrincipalLookupError:
                sender = None

            title = u''
            avatar = u''
            space = u''

            profile = IPersonalProfile(sender, None)
            if profile is not None:
                avatar = profile.avatarUrl(request)
                title = profile.title

                space = profile.space
                if space is not None:
                    space = '%s/'%absoluteURL(space, request)

            yield {'name': message.__name__,
                   'status': message.__status__,
                   'sender': title.strip(),
                   'profile': space,
                   'date': message.__date__,
                   'title': message.title,
                   'avatar': avatar}
