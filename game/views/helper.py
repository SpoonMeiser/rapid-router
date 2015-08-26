# -*- coding: utf-8 -*-
# Code for Life
#
# Copyright (C) 2015, Ocado Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ADDITIONAL TERMS – Section 7 GNU General Public Licence
#
# This licence does not grant any right, title or interest in any “Ocado” logos,
# trade names or the trademark “Ocado” or any other trademarks or domain names
# owned by Ocado Innovation Limited or the Ocado group of companies or any other
# distinctive brand features of “Ocado” as may be secured from time to time. You
# must not distribute any modification of this program using the trademark
# “Ocado” or claim any affiliation or association with Ocado or its employees.
#
# You are not authorised to use the name Ocado (or any of its trade names) or
# the names of any author or contributor in advertising or for publicity purposes
# pertaining to the distribution of this program, without the prior written
# authorisation of Ocado.
#
# Any propagation, distribution or conveyance of this program must include this
# copyright notice and these terms. You must not misrepresent the origins of this
# program; modified versions of the program must be marked as such and not
# identified as the original program.
from __future__ import division

import os

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import RequestContext
from game.forms import AvatarUploadForm, AvatarPreUploadedForm
from game.models import Decor


def renderError(request, title, message):
    """ Renders an error page with passed title and message.

    **Context**

    ``RequestContext``
    ``title``
        Title that is to be used as a title and header of the page. String.
    ``message``
        Message that will be shown on the error page. String.

    **Template:**

    :template:`game/error.html`
    """
    context = RequestContext(request, {
        'title': title,
        'message': message
    })
    return render(request, 'game/error.html', context_instance=context)


def getDecorElement(name, theme):
    """ Helper method to get a decor element corresponding to the theme or a default one."""
    try:
        return Decor.objects.get(name=name, theme=theme)
    except ObjectDoesNotExist:
        return Decor.objects.filter(name=name)[0]


def renderAvatarChoice(request):
    """ Helper method for settings view. Generates and processes the avatar changing forms.
    """
    x = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(x, 'portal/static/portal/img/avatars')
    img_list = os.listdir(path)
    userProfile = request.user.userprofile
    avatar = userProfile.avatar
    avatarUploadForm = AvatarUploadForm(request.POST or None, request.FILES)
    avatarPreUploadedForm = AvatarPreUploadedForm(request.POST or None, my_choices=img_list)
    if request.method == 'POST':
        if "pre-uploaded" in request.POST and avatarPreUploadedForm.is_valid:
            avatar = avatarPreUploadedForm.data.get('pre-uploaded', False)
        elif "user-uploaded" in request.POST and avatarUploadForm.is_valid():
            avatar = request.FILES.get('avatar', False)
        userProfile.avatar = avatar
        userProfile.save()
    return avatarUploadForm, avatarPreUploadedForm
