import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctorfinder.settings')
django.setup()

from doctors.models import Specialization

# List of common specializations with their descriptions and icons
specializations = [
    {
        'name': 'Cardiology',
        'description': 'Deals with disorders of the heart and the cardiovascular system.',
        'icon': 'bi bi-heart-pulse'
    },
    {
        'name': 'Dermatology',
        'description': 'Focuses on the diagnosis and treatment of skin disorders.',
        'icon': 'bi bi-bandaid'
    },
    {
        'name': 'Neurology',
        'description': 'Deals with disorders of the nervous system, including the brain and spinal cord.',
        'icon': 'bi bi-lightning'
    },
    {
        'name': 'Ophthalmology',
        'description': 'Deals with the diagnosis and treatment of eye disorders.',
        'icon': 'bi bi-eye'
    },
    {
        'name': 'Orthopedics',
        'description': 'Focuses on conditions involving the musculoskeletal system.',
        'icon': 'bi bi-universal-access'
    },
    {
        'name': 'Pediatrics',
        'description': 'Deals with the medical care of infants, children, and adolescents.',
        'icon': 'bi bi-emoji-smile'
    },
    {
        'name': 'Psychiatry',
        'description': 'Focuses on the diagnosis, prevention, and treatment of mental disorders.',
        'icon': 'bi bi-person-hearts'
    },
    {
        'name': 'Gynecology',
        'description': 'Deals with the health of the female reproductive system.',
        'icon': 'bi bi-gender-female'
    },
    {
        'name': 'Urology',
        'description': 'Focuses on diseases of the urinary tract and the male reproductive system.',
        'icon': 'bi bi-droplet'
    },
    {
        'name': 'Oncology',
        'description': 'Deals with the prevention, diagnosis, and treatment of cancer.',
        'icon': 'bi bi-shield-plus'
    },
    {
        'name': 'Endocrinology',
        'description': 'Focuses on disorders of the endocrine system and its specific hormones.',
        'icon': 'bi bi-activity'
    },
    {
        'name': 'Gastroenterology',
        'description': 'Deals with disorders of the digestive system.',
        'icon': 'bi bi-capsule'
    },
]

# Add specializations if they don't exist
for spec in specializations:
    Specialization.objects.get_or_create(
        name=spec['name'],
        defaults={
            'description': spec['description'],
            'icon': spec['icon']
        }
    )

print(f"Added {len(specializations)} specializations. Current count: {Specialization.objects.count()}") 