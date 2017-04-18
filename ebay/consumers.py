from channels import Group
import random
from .models import Player, Group as OtreeGroup, Constants
import json
import time
from channels.sessions import channel_session



# Connected to chat-messages
def braintree_process(message):
    print('BRAIN!!!!!!$$$$$$$', message.content['group_pk'])
    Group('group1').send({
        "text": json.dumps(message.content['price']),
    })
    # a = 1/0



@channel_session
def ws_connect(message, group_name):
    print('GROUP NAME::::: ', group_name)
    Group(group_name).add(message.reply_channel)
    print('NEW MEMBER CONNECTED...')
    Group(group_name).send({
        "text": json.dumps('test message'),
    })


@channel_session
def ws_message(message, group_name):
    print('GOT THE MESSAGE::::', message.content['text'])
    group_id = group_name[5:]
    mygroup = OtreeGroup.objects.get(id=group_id)
    textforgroup = json.dumps({
                                "price": mygroup.price,
                                })
    Group(group_name).send({
        "text": textforgroup,
    })

    textforgroup = json.dumps({
                                "price": mygroup.price,
                                })
    Group(group_name).send({
        "text": textforgroup,
    })


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message, group_name):
    Group(group_name).discard(message.reply_channel)
