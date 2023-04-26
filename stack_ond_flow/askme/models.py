USER = [
    {
    "id": i,
    "avatar": f"img/avatar{i % 3 + 1}.jpeg",
    "name": f"User{i}",
    "rating": 100 * i
    } for i in range(3)
]

QUESTIONS = [
    {
    'id': i,
    'user': USER[i],
    'title': f'Question {i}',
    'text': f'Text {i}',
    'rating': 100 * i, 
    'time_ago': f'{i} minutes ago'
    } for i in range(3)
]

ANSWERS = [
    {
    'id': i,
    'user': USER[i % 3],
    'rating': 100 - i,
    'text': f'Text{i}',
    'right_flag': False,
    'time_ago': f"{i} minutes ago"
    } for i in range(0, 100)
]

TAGS = [
    {
        "id": i,
        "name": f"Tag {i}"
    } for i in range(12)
]


