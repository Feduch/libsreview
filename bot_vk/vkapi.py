import vk
import random
import requests
from bot_vk.appsettings import *

session = vk.Session()
api = vk.API(session, v=5.84)


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)


def post_to_wall(groip_id, message, attachment=""):
    api.wall.post(access_token=access_token_awaik_user, owner_id="-"+str(groip_id), message=message, attachment=attachment)


def get_random_wall_picture(group_id):
    max_num = api.photos.get(owner_id=group_id, album_id='wall', count=0, access_token=service_key)['count']
    num = random.randint(1, max_num)
    photo = api.photos.get(owner_id=group_id, album_id='wall', count=1, offset=num, access_token=service_key)['items'][0]['id']
    attachment = 'photo' + str(group_id) + '_' + str(photo)
    return attachment

def get_all_group_members(group_id, offset=0, num=40000):
    members = api.groups.getMembers(group_id=group_id, access_token=token, offset=offset, num=num)
    return members

def send_message_group_members(user_ids, message, attachment=""):
    api.messages.send(user_ids=user_ids, message=message, attachment=attachment, access_token=token)


