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

        url1 = "https://firebasestorage.googleapis.com/v0/b/grade5-2448a.appspot.com/o/Absolute_Reality_v16_Electricity_Energy_Current_0.jpeg?alt=media&token=3e3f7923-9ef5-4dca-9ebf-72ba5cb6d0c0"
        url2 = "https://firebasestorage.googleapis.com/v0/b/grade5-2448a.appspot.com/o/Absolute_Reality_v16_mechanics_force_physics_engine_0.jpeg?alt=media&token=cc168092-1bb3-4900-b8c5-490c5b2ab66d"
        url3 = "https://firebasestorage.googleapis.com/v0/b/grade5-2448a.appspot.com/o/Pixel_Art_physics_astronomy_galaxy_universe_2.jpeg?alt=media&token=35abd779-11a5-477e-859b-fec90d664a1e"
        url4 = "https://firebasestorage.googleapis.com/v0/b/grade5-2448a.appspot.com/o/Absolute_Reality_v16_optics_Physics_Light_spectrum_fiber_0.jpeg?alt=media&token=77419465-e338-415e-899d-6cb1d3c305ed"
        url5 = "https://firebasestorage.googleapis.com/v0/b/grade5-2448a.appspot.com/o/Pixel_Art_physics_astronomy_planets_stars_2.jpeg?alt=media&token=e6701665-90f4-48c3-9057-21bbf765f8b5"
        video_url = "https://www.youtube.com/watch?v=ZSt9tm3RoUU"
        image_urls = [url1, url2, url3, url4, url5]
        # Create modules for each chapter
        for chapter in Chapter.objects.all():
            for i in range(1, 11):
                text_content = TextField.objects.create(text=fake.paragraph(nb_sentences=500), user=chapter.user)
                image_content = ImageField.objects.create(
                    image=image_urls,  
                    user=chapter.user
                )
                # print(f"Video URL being inserted: {video_url}")  # debugging line
                # self.stdout.write(self.style.SUCCESS(f"Video URL being inserted: {video_url}"))
                video_content = VideoField.objects.create(video=video_url, user=chapter.user)

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
