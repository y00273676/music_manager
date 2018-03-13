import tornado.web

class PageNumModule(tornado.web.UIModule):
    def render(self, pageinfo):
        return self.render_string('modules/pagenum.html', pageinfo=pageinfo)
