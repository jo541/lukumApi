from app import api, resource


@api.route('/hello')
class HelloWorld(resource):
    def get(self):
        return {'hello': 'world'}
