from __future__ import absolute_import
import os
from celery import Celery
from django.core.cache import cache
import time
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
app = Celery("Core")
app.config_from_object('django.conf:settings', namespace='CELERY')

channel_layer = get_channel_layer()


@app.task
def print_ms():
    print('nigga')


@app.task
async def check_game_end(room_code: str):
    print('Check end', room_code)
    room_data = cache.get(room_code)
    room_data['is_end'] = True
    room_data['status'] = 'Time is over'
    # Correct the time of move if a connection occurs between moves
    time_delta = int(time.time()) - room_data['time_last_action']
    match room_data['current_player']:
        case 'player1':
            room_data['player1_time'] -= time_delta
        case 'player2':
            room_data['player2_time'] -= time_delta
    await channel_layer.group_send(
        room_code, room_data
    )

    await channel_layer.group_send(
        room_code,
        {
            'type': 'game.end'
        }
    )
    cache.set(room_code, room_data)


app.autodiscover_tasks()
