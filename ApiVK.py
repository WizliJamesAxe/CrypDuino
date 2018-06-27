import requests


class ApiVK:
    URL = "https://api.vk.com/method/"

    def __init__(self, token, version='5.74'):
        self.version_and_token = {'v': version, 'access_token': token}

    def validate_and_get_name(self):
        req = requests.post(self.URL + 'account.getProfileInfo', data=self.version_and_token)
        try:
            response = req.json()['response']
        except IndexError:
            return False
        return response['first_name'] + ' ' + response['last_name']

    def send_message(self, user_id, message='', attachment=''):
        params = {'user_id': str(user_id), 'message': message, 'attachment': attachment}
        params.update(self.version_and_token)
        req = requests.post(self.URL+'messages.send', data=params)
        return req.json()

    def get_unread(self, user_id, last_mes):
        params = {'count': 10}
        params.update(self.version_and_token)
        req = requests.post(self.URL + 'messages.get', data=params)
        answer = req.json()['response']['items']
        new_messages = []
        for i in answer:
            if (i['user_id'] == user_id)and(i['title'] == ''):
                if i['id'] > last_mes:
                    new_messages.append([i['body'], i['id']])
                else:
                    break
        new_messages.reverse()
        return new_messages
