from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from grade5.models import Subject, Chapter, Module, TextField, ImageField, VideoField, MCQ, Content, MCQSet  # Replace 'your_app_name' with the actual app name

class Command(BaseCommand):
    help = 'Populates the database with fake data for testing.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create users
        user_list = [
            {'username': 'Alice', 'password': '1234'},
            {'username': 'Bob', 'password': '1234'},
            {'username': 'Bill', 'password': '1234'},
        ]

        for user_data in user_list:
            user = User.objects.create_user(username=user_data['username'], password=user_data['password'])

            # Create subjects for each user
            subject_names = ['phy', 'math', 'chem', 'bio']
            for name in subject_names:
                Subject.objects.create(name=name, user=user)

            # Create chapters for each subject of the user
            for subject in Subject.objects.filter(user=user):
                for i in range(1, 11):
                    Chapter.objects.create(name=f'Chapter {i}', subject=subject, user=user)

        # Create modules for each chapter
        for chapter in Chapter.objects.all():
            for i in range(1, 11):
                text_content = TextField.objects.create(text=fake.paragraph(nb_sentences=5), user=chapter.user)
                image_content = ImageField.objects.create(
                    image=[fake.image_url() for _ in range(4)],
                    user=chapter.user
                )
                video_content = VideoField.objects.create(video=fake.url(), user=chapter.user)

                mcq_set = MCQSet.objects.create(user=chapter.user)

                for _ in range(3):
                    MCQ.objects.create(
                        question_title=fake.sentence(),
                        choice1=fake.word(),
                        choice2=fake.word(),
                        choice3=fake.word(),
                        choice4=fake.word(),
                        correct_choice=fake.random_int(min=1, max=4),
                        mcq_set=mcq_set
                    )

                content_obj = Content.objects.create(
                    text=text_content,
                    image=image_content,
                    video=video_content,
                    mcq_set=mcq_set
                )

                Module.objects.create(name=f'Module {i}', chapter=chapter, content=content_obj, user=chapter.user)

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
