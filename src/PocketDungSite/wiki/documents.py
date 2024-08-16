from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

#наша модель статье, к которй мы хотим прекрутить elsaticsearch 
from .models import Info


@registry.register_document
class InfoDocument(Document):
    class Index:
        name = "infos"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Info
        fields = ["i_name", "i_text", ]