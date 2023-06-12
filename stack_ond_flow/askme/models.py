from django.db import models

USER = [
    {
        'id': id,
        'avatar': f'img/avatar{id+1}.jpeg',
        'name': f'User{id}',
        'rating': 100 * id
    } for id in range(5)
]

TAGS = [
    {
        'id': id,
        'name': f'Tag {id}',
    } for id in range(12)
]

ANSWERS = [
    {
        'id': id,
        'user': USER[id % 3],
        'rating': 100 - id,
        'text': f'Text{id}',
        'right_flag': False,
        'time_ago': f"{id} minutes ago"
    } for id in range(3)
]

QUESTIONS = [
    {
        'id': id,
        'user': USER[id],
        'title': f'Question {id}',
        'text': f'Text {id}',
        'rating': 100 * id, 
        "answers_amount": id + 1,
        'answers': ANSWERS[:id + 1],
        'tags': TAGS[id % 8:id % 8 + 3],
        'time_ago': f'{id} minutes ago'
    } for id in range(5)
]
