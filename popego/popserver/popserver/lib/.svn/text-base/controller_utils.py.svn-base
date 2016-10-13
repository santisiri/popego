# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

import popserver.model as model
from pylons.controllers.util import abort

def find_widget(username, id):
    # Eagerload a user
    widget = model.Widget.query.filter(model.Widget.user.has(model.User.username == username)) \
        .filter_by(id=id).first()
    if widget is None:
        abort(404, "Inexistent Widget")

    return widget

def build_json_response(status, statusText=None, description=None):
    r =  {"status": status}
    if statusText is not None:
        r['statusText'] = statusText
    if description is not None:
        r['description'] = description

    return r


