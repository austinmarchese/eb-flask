import json

from flask import Flask, request
from flask_api import status
import stanza
stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors="TOKENIZE,POS,NER")
app = Flask(__name__)
import os

@app.route('/actuator')
def actuator():
    ent = nlp("Barack Obama was born in Hawaii.").entities
    print(ent)

    return str(ent), status.HTTP_200_OK


# @app.route('/test', methods=["GET"])
# def test():
#     description = request.args.get('description')
#     if description is None or len(description) == 0:
#         return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
#     else:
#         pass
#     tags = Check().ab(description)
#     return json.dumps(tags)

@app.route('/getTagsFromBody', methods=["GET", "POST"])
def getTagsFromBody():
    try:
        # request_text = request.data.decode('utf-8')
        # print(request_text)
        print(request.json)
        data = request.json
        # content = json.loads(request_text)
        # description = content['description']
        # print(descripti)
        description = data['description']
        print(description)
    except Exception as e:
        print(e)
        return "please provide description in json %s" % e, status.HTTP_400_BAD_REQUEST

    return json.dumps(description)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    a = os.popen('hostname').read()
    if 'Austin' not in a:
        app.debug = True
        app.run()
    else:
        app.run(host="0.0.0.0", port=5005, debug=False)
