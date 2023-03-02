from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from models import Session, Ads
from schema import validate_create_post
from models import HttpError

app = Flask('my_app')


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_post(post_id: int, session: Session):
    post = session.query(Ads).get(post_id)
    if post is None:
        raise HttpError(status_code=404, message='post not found')
    return post


class PostView(MethodView):

    def get(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            return jsonify({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'creation_date': post.creation_date.isoformat(),
                'owner_id': post.owner_id, })

    def post(self):
        json_data = validate_create_post(request.json)

        with Session() as session:
            new_post = Ads(**json_data)
            session.add(new_post)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(status_code=400, message='no user in db')
            return jsonify({
                'id': new_post.id,
                'title': new_post.title,
                'description': new_post.description,
                'creation_date': new_post.creation_date.isoformat(),
                'owner_id': new_post.owner_id, })

    def delete(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            session.delete(post)
            session.commit()
        return jsonify({'status': 'post deleted successfully'})


app.add_url_rule('/advertisement/<int:post_id>', view_func=PostView.as_view('advertisement'), methods=['GET', 'DELETE'])
app.add_url_rule('/advertisement', view_func=PostView.as_view('advertisement_post'), methods=['POST'])

if __name__ == '__main__':
    app.run()
