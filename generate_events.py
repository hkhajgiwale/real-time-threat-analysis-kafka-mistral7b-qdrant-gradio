from faker import Faker
from faker_security.providers import SecurityProvider
import random
from confluent_kafka import Producer
import json
import time
## Kafka producer config settings

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
})

def generate_cybersecurity_events():
    """
    This generates the fake cybersecurity events required for streaming to data
    """
    fake = Faker()
    fake.add_provider(SecurityProvider)
    fake_event = {}

    ## User data
    fake_event["username"] = fake.user_name()
    fake_event["ip_address"] = fake.ipv4()
    fake_event["user_agent"] = fake.user_agent() 

    ## Attack type
    attack_type_options = ["reconnaissance", "denial-of-service", "phishing", "man-in-the-middle",
                           "social engineering", "malware", "privilege escalation",
                           "data exfiltration", "web application attack", "remote access attack"]
    fake_event['attack_type'] = random.choice(attack_type_options)

    # Threat Actor
    threat_actor_options = ["Script Kiddie", "Black Hat Hacker", "APT Group", "Insider Threat"]
    fake_event["threat_actor"] = random.choice(threat_actor_options)

    fake_event['cwe'] = fake.cwe()
    fake_event['cve'] = fake.cve()
    fake_event['affected_resource'] = fake.file_path()
    fake_event['timestamp'] = fake.date_time().isoformat()
    return fake_event


while True:
    fake_event = generate_cybersecurity_events()
    fake_event_str = json.dumps(fake_event)
    print(fake_event_str)
    producer.produce('threat-analytics-topic', fake_event_str)
    #producer.poll(0)
    #time.sleep(5)