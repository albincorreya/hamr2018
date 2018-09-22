from util import *
from flask import Flask
from flask_restplus import Resource, Api,reqparse
from flask import request, jsonify
from flask import Flask
from flask_restplus import Resource, Api,reqparse
from flask import Flask, request, jsonify
import requests
import json
import werkzeug
import parsers
import time


app = Flask(__name__)
api = Api(app)

@api.route('/words_to_music')
class WordsToMusic(Resource):
    @api.expect(parsers.file_upload)
    def get(self):
        generative_other = 'bad and this is crazy but you look right'
        text = generative_other          
        output_file = words_to_music(text)
        return jsonify('Output file wrote at {}'.format(output_file))

@api.route('/sentence_to_music')
class Sentence_To_Music(Resource):
    @api.expect(parsers.file_upload)
    def get(self):
        text_input = 'Try to chase me\nSo call me, maybe\nHey I just met you\n'
        output_file = sentence_to_music(text_input)
        return jsonify('Output file wrote at {}'.format(output_file))
    
            
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)
