from confluent_kafka import Consumer, KafkaException
from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
import uuid

consumer_config = {
    'bootstrap.servers' : 'localhost:9092',
    'group.id' : 'cybersecurity-group',
    'auto.offset.reset': 'earliest'
}

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

qdrant_client = QdrantClient(host="localhost", port=6333)

docs = [{'username': 'jenniferjohnson', 'ip_address': '85.154.183.245', 'user_agent': 'Opera/8.14.(Windows CE; da-DK) Presto/2.9.161 Version/12.00', 'attack_type': 'denial-of-service', 'threat_actor': 'APT Group', 'cwe': 'CWE-794', 'cve': 'CVE-1998-9195', 'affected_resource': '/may/next.mp4', 'timestamp': '1983-12-06T22:07:47.976428'}, {'username': 'heathtracy', 'ip_address': '223.171.200.167', 'user_agent': 'Mozilla/5.0 (iPad; CPU iPad OS 17_2 like Mac OS X) AppleWebKit/536.1 (KHTML, like Gecko) FxiOS/12.6f8148.0 Mobile/06N929 Safari/536.1', 'attack_type': 'malware', 'threat_actor': 'APT Group', 'cwe': 'CWE-490', 'cve': 'CVE-2012-7902', 'affected_resource': '/our/rule.mp3', 'timestamp': '2003-06-04T23:44:00.904300'}]

qdrant_client.create_collection(
   collection_name = "cybersecurity_embeddings",
   vectors_config = VectorParams(
       size = model.get_sentence_embedding_dimension(),
       distance = Distance.COSINE
   )
)

for doc in docs:
    event_id = str(uuid.uuid4())
    username_vector = model.encode(doc['username'])
    user_agent_vector = model.encode(doc['user_agent'])
    attack_type_vector = model.encode(doc['attack_type'])
    threat_actor_vector = model.encode(doc['threat_actor'])
    cwe_vector = model.encode(doc['cwe'])
    cve_vector = model.encode(doc['cve'])
    affected_resource_vector = model.encode(doc['affected_resource'])

    combined_vector = username_vector + user_agent_vector + attack_type_vector + threat_actor_vector + cwe_vector + cve_vector + affected_resource_vector

    qdrant_client.upsert(
        collection_name="cybersecurity_embeddings", 
        points = [
            models.PointStruct (
                id = event_id,
                payload = {
                    "username": doc['username'],
                    "ip_address": doc['ip_address'],
                    "user_agent": doc['user_agent'],
                    "attack_type": doc['attack_type'],
                    "threat_actor": doc['threat_actor'],
                    "cwe": doc['cwe'],
                    "cve": doc['cve'],
                    "affected_resource": doc['affected_resource'],
                    "timestamp": doc['timestamp']
                },
                vector = combined_vector.tolist()  
            )
        ]
    )

print("Data Inserted")

