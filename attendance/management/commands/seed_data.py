from django.core.management.base import BaseCommand
from attendance.models import Teacher, Student 

class Command(BaseCommand):
    help = 'Seeds dummy data matching the exact schema for Teachers and Students.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database seeding...')

        # 1. SEED TEACHER DATA (Uses 'email' and 'name')
        teacher, t_created = Teacher.objects.get_or_create(
            email='john.smith@school.com',
            defaults={
                'name': 'John Smith'
            }
        )
        if t_created:
            self.stdout.write(f"Successfully created Teacher: {teacher.name}")
        else:
            self.stdout.write(f"Teacher {teacher.name} already exists.")

        # 2. SEED STUDENT DATA (Uses 'roll_number' and 'name')
        students_dataset = [
            {'name': 'Alice Jones', 'roll_number': 'STU001'},
            {'name': 'Bob Miller', 'roll_number': 'STU002'},
            {'name': 'Charlie Brown', 'roll_number': 'STU003'},
            {'name': 'Diana Prince', 'roll_number': 'STU004'},
        ]

        for data in students_dataset:
            # Look up by unique roll number instead of email
            student, s_created = Student.objects.get_or_create(
                roll_number=data['roll_number'],
                defaults={
                    'name': data['name']
                }
            )
            if s_created:
                self.stdout.write(f"Successfully created Student: {student.name} ({student.roll_number})")
            else:
                self.stdout.write(f"Student {student.name} already exists.")

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))
