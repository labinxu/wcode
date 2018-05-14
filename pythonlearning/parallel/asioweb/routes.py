import views

def setup_routes(app):
    app.router.add_get('/', views.index)
    app.router.add_post('/post', views.exam_post)
    app.router.add_get('/websocket', views.websocket_handler)

