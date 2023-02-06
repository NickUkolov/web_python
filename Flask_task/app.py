from flask import Flask, request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from db import Session, Post
from errors import HttpError
from schema import validate_create_post

app = Flask(__name__)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


def get_post(post_id: int, session: Session):
    post = session.query(Post).get(post_id)
    if post is None:
        raise HttpError(status_code=404, message='post not found')
    return post


class PostView(MethodView):

    def get(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            return jsonify({
                'post_id': post.id,
                'title': post.title,
                'description': post.description,
                'owner': post.owner,
                'created_at': post.created_at.isoformat(),
            })

    def post(self):
        json_data = validate_create_post(request.json)

        with Session() as session:
            new_post = Post(**json_data)
            session.add(new_post)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(status_code=400, message='no user in db')
            return jsonify({
                'id': new_post.id,
                'title': new_post.title,
                'description': new_post.description,
                'owner': new_post.owner,
                'created_at': new_post.created_at.timestamp(),
            })

    def delete(self, post_id: int):
        with Session() as session:
            post = get_post(post_id, session)
            session.delete(post)
            session.commit()
        return jsonify({'status': 'post deleted successfully'})


app.add_url_rule('/posts/<int:post_id>', view_func=PostView.as_view('posts'), methods=['GET', 'DELETE'])
app.add_url_rule('/posts', view_func=PostView.as_view('posts_post'), methods=['POST'])


if __name__ == '__main__':
    app.run()
