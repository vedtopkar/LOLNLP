import web
import recommendation_engine

urls = (
    '/', 'index',
    '/recommend', 'recommend',
    '/recommend/html', 'recommend_html'
)


class index:
    def GET(self):
        raise web.seeother('/static/index.html')

class recommend:
    def GET(self):
        user_input = web.input(q=None)
        query = user_input.q

        print 'Received query: {}'.format(query)
        if query:
            return recommendation_engine.recommend_gif(query)
        else:
            return 'Please enter a query'

class recommend_html:
    def GET(self):
        web.header('Content-Type', 'text/html')
        query = web.input().q

        print 'Received query: {}'.format(query)
        if query:
            url= recommendation_engine.recommend_gif(query)
            return '<img src={0} />'.format(url)
        else:
            return 'Please enter a query'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()