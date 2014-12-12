import web
import content_analysis
import sentiment_analysis
import recommendation_engine

urls = (
    '/', 'index'
)


class index:
    def GET(self):
        raise web.seeother('/static/index.html')



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()