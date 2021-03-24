from app.app import create_app
from app.utils.utils import encrypt

app = create_app()


@app.after_request
def after_request(response):
    response.data = encrypt(response.data)
    return response


app.run()
