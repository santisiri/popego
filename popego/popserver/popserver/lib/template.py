import pylons
from pylons.templating import Buffet
from pylons import config
import popserver.lib.helpers as h

class MyBuffet(Buffet):
    def _update_names(self, ns):
        return ns

def_eng = config['buffet.template_engines'][0]
buffet = MyBuffet(
    def_eng['engine'],
    template_root=def_eng['template_root'],
    **def_eng['template_options']
)

for e in config['buffet.template_engines'][1:]:
    buffet.prepare(
        e['engine'],
        template_root=e['template_root'],
        alias=e['alias'],
        **e['template_options']
    )

class State:
    pass

c = State()
c.user = 'None'

def make_template():
    return buffet.render(
        template_name="/website/home/index.mako",
        namespace=dict(h=h, c=State())
    ).replace("%", "%%").replace("FORM_ACTION", "%s")
