import random
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

from askme.models import Question, Answer, Tag

fake = Faker()

num_users = 100
users = []
for i in range(num_users):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    user = User.objects.create_user(username=username, email=email, password=password)
    users.append(user)

num_questions = 120
questions = []
for i in range(num_questions):
    title = fake.sentence()
    content = fake.paragraph()
    user = random.choice(users)
    pub_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
    question = Question.objects.create(title=title, content=content, user=user, pub_date=pub_date)
    questions.append(question)

num_answers = 120
for i in range(num_answers):
    content = fake.paragraph()
    question = random.choice(questions)
    user = random.choice(users)
    pub_date = fake.date_time_between(start_date=question.pub_date, end_date='now', tzinfo=timezone.get_current_timezone())
    Answer.objects.create(content=content, question=question, user=user, pub_date=pub_date)

num_tags = 120
tags = []
for i in range(num_tags):
    name = fake.word()
    tag = Tag.objects.create(name=name)
    tags.append(tag)

