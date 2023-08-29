from django.core.management.base import BaseCommand
from faker import Faker
from grade5.models import Subject, Chapter, Module, TextField, ImageField, VideoField, MCQ, Content, MCQSet  # Assuming MCQSet is the model to hold a set of MCQs

class Command(BaseCommand):
    help = 'Populates the database with fake data for testing.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create subjects
        subject_names = ['phy', 'math', 'chem', 'bio']
        for name in subject_names:
            Subject.objects.create(name=name)

        # Create chapters for each subject
        for subject in Subject.objects.all():
            for i in range(1, 11):
                Chapter.objects.create(name=f'Chapter {i}', subject=subject)

        for chapter in Chapter.objects.all():
            for i in range(1, 11):
                # Create text, image, and video content
                text_content = TextField.objects.create(text=fake.paragraph(nb_sentences=5))
                image_content = ImageField.objects.create(
                    image=[fake.image_url() for _ in range(4)]
                )
                video_content = VideoField.objects.create(video=fake.url())

                # # Create a set of MCQs
                # mcq_set = MCQSet.objects.create()  # Assuming you have an MCQSet model

                # # Create MCQs and link them to the MCQSet
                # for _ in range(3):  # 3 MCQs per module
                #     mcq_content = MCQ.objects.create(
                #         question_title=fake.sentence(),
                #         choice1=fake.word(),
                #         choice2=fake.word(),
                #         choice3=fake.word(),
                #         choice4=fake.word(),
                #         correct_choice=fake.random_int(min=1, max=4),
                #         mcq_set=mcq_set  # Linking the MCQ to the MCQSet
                #     )
                    
                # Create a Content object linking to text, image, video, and MCQSet
                content_obj = Content.objects.create(
                    text=text_content,
                    image=image_content,
                    video=video_content,
                    # mcq=mcq_set  # Linking the MCQSet to the content
                )

                # Create a Module linking to the content
                Module.objects.create(name=f'Module {i}', chapter=chapter, content=content_obj)

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
