from flask_restful import Resource, reqparse
from models import User, Survey, Question, RevokedTokenModel
from datetime import datetime
from flask import jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class UserRegistration(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('email', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('password', help = 'This field cannot be blank', required = True, location='headers')

        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        if User.find_by_email(data['email']):
            return {'message': 'User with email {} already exists'.format(data['email'])}

        new_user = User(
            login = data['username'],
            email = data['email'],
            paswd = User.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('password', help = 'This field cannot be blank', required = True, location='headers')

        data = parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.paswd):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.login),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class SurveyGet(Resource):
    @jwt_required
    def get(self):
        current_username = get_jwt_identity()
        u = User.find_by_username(current_username)

        user_surveys = Survey.query.filter_by(idUser = u.idUser).all()
        if not user_surveys:
            return {'message': f'User {current_username} has no surveys'}

        return jsonify(surveys=[i.serialize for i in user_surveys])

class SurveyActive(Resource):
    def get(self):
        active_surveys = Survey.query.filter(Survey.isActive == True, Survey.dueDate > datetime.now()).all()
        if not active_surveys:
            return {'message': 'There are no active surveys'}
        return jsonify(surveys=[i.serialize for i in active_surveys])

class SurveyAdd(Resource):
    @jwt_required
    def post(self):
        current_username = get_jwt_identity()
        u = User.find_by_username(current_username)

        parser = reqparse.RequestParser()
        parser.add_argument('name', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('desc', location='headers')
        parser.add_argument('duedate', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('isactive', location='headers')

        data = parser.parse_args()

        boolActive = True if hasattr(data, 'isactive') and data['isactive'] == 'True' else False

        new_survey = Survey(
            name = data['name'],
            desc = data['desc'],
            dueDate = data['duedate'],
            isActive = boolActive,
            idUser = u.idUser
        )

        try:
            new_survey.save_to_db()
            return {'message': 'Survey {} was created'.format(data['name'])}
        except:
            return {'message': 'Something went wrong'}, 500

class QuestionAdd(Resource):
    @jwt_required
    def post(self):
        current_username = get_jwt_identity()
        u = User.find_by_username(current_username)

        parser = reqparse.RequestParser()
        parser.add_argument('idSurvey', help = 'This field cannot be blank', required = True, location='headers')
        parser.add_argument('content', location='headers')
        parser.add_argument('type', help = 'This field cannot be blank', required = True, location='headers')

        data = parser.parse_args()

        requested_survey = Survey.query.get(data['idSurvey'])
        if requested_survey is None:
            return {'message': f'Survey doesn\'t exist'}

        #Check if user is owner of that survey
        if not (u.idUser == requested_survey.idUser):
            return {'message': f'User {current_username} not permited'}

        print(Survey.query.get(data['idSurvey']))
        new_question = Question(
            content = data['content'],
            type = data['type'],
            idSurvey = data['idSurvey'],
        )

        try:
            new_question.save_to_db()
            return {'message': 'Question was added'}
        except:
            return {'message': 'Something went wrong'}, 500

class AllUsers(Resource):
    def get(self):
        return User.return_all()

    def delete(self):
        return User.delete_all()
