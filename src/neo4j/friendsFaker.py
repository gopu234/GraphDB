from faker import Faker
import random
import csv


faker = Faker()

PERSON_COUNT = 100
RELATIONSHIP_COUNT = 300

def generate_fake_data(filename, num_records):

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Age','City','Email'])

        for i in range(num_records):
            writer.writerow([
                faker.name(),
                random.randint(18, 65),
                faker.city(),
                faker.email()
            ])


generate_fake_data('people.csv', 100)


