import web

urls = (
    '/', 'index'
)

print 'initialized'

class index:
    def GET(self):
        raise web.seeother('/static/index.html')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()