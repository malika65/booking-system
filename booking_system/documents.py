from django.db.models.fields.files import ImageFieldFile
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from rest_framework.fields import ImageField

from authe.models import User
from .models.hotel_models import Hotel, Room, HotelImage
from .models.country_models import Country, City
from .models.characteristic_models import (
    Category,
    FoodCategory,
    FacilitiesAndServicesHotels,
    FacilitiesAndServicesRooms,
    HotelCategoryStars,
    Characteristics
)
from .models.booking_models import Booking
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import TextField


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
    name_ru = TextField()
    name_en = TextField()

    class Django:
        model = Category
        fields = []


@registry.register_document
class FacilitiesAndServicesHotelsDocument(Document):
    class Index:
        name = 'facilities_hotels'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    hotel_category_name_ru = TextField()
    hotel_category_name_en = TextField()

    class Django:
        model = FacilitiesAndServicesHotels
        fields = []


@registry.register_document
class FacilitiesAndServicesRoomsDocument(Document):
    class Index:
        name = 'facilities_rooms'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    room_category_name_ru = TextField()
    room_category_name_en = TextField()

    class Django:
        model = FacilitiesAndServicesRooms
        fields = []


@registry.register_document
class FoodCategoryDocument(Document):
    class Index:
        name = 'food_category_rooms'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    food_category_name_ru = TextField()
    food_category_name_en = TextField()

    class Django:
        model = FoodCategory
        fields = []


@registry.register_document
class HotelCategoryStarsDocument(Document):
    class Index:
        name = 'hotel_category_stars'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    hotel_category_name_ru = TextField()
    hotel_category_name_en = TextField()

    class Django:
        model = HotelCategoryStars
        fields = [
            'hotel_category_stars'
        ]


@registry.register_document
class CountryDocument(Document):
    class Index:
        name = 'country'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    country_name_ru = TextField()
    country_name_en = TextField()

    class Django:
        model = Country
        fields = []


@registry.register_document
class CityDocument(Document):
    country_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'country_name_ru': fields.TextField(),
        'country_name_en': fields.TextField()
    })

    class Index:
        name = 'city'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    city_name_ru = TextField()
    city_name_en = TextField()

    class Django:
        model = City
        fields = []


@registry.register_document
class CharacteristicsDocument(Document):
    class Index:
        name = 'characteristics'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    name_ru = TextField()
    name_en = TextField()

    class Django:
        model = Characteristics
        fields = [
            'capacity',
        ]


@registry.register_document
class RoomDocument(Document):
    category_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'room_category_name_ru': fields.TextField(),
        'room_category_name_en': fields.TextField(),
    })
    characteristics_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name_ru': fields.TextField(),
        'name_en': fields.TextField(),
        'capacity': fields.IntegerField(),
    })
    room_name_ru = TextField()
    room_name_en = TextField()
    room_description_ru = TextField()
    room_description_en = TextField()

    class Index:
        name = 'room'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Room
        fields = [
            'price',
            'child_capacity'
        ]


@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = User
        fields = [
            'email',
        ]


@registry.register_document
class HotelImageDocument(Document):
    image_url = StringField()

    class Index:
        name = 'hotel_images'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = HotelImage


@registry.register_document
class HotelDocument(Document):
    city = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'city_name_ru': StringField(fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }),
            'city_name_en': StringField(fields={
                'raw': KeywordField(),
                'suggest': fields.CompletionField(),
            }),
            'country_id': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'country_name_ru': StringField(fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField()
                    }),
                    'country_name_en': StringField(fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField()
                    }),
                }
            )
        }
    )
    food_category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'food_category_name_ru': fields.TextField(),
        'food_category_name_en': fields.TextField(),
    })
    hotel_category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'hotel_category_name_ru': fields.TextField(),
        'hotel_category_name_en': fields.TextField(),
        'hotel_category_stars': fields.TextField(),
    })
    category_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'hotel_category_name_ru': fields.TextField(),
        'hotel_category_name_en': fields.TextField(),
    })
    room_id = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'room_name_ru': StringField(),
            'room_name_en': StringField(),
            'room_description_ru': fields.TextField(),
            'room_description_en': fields.TextField(),
            'price': fields.IntegerField(),
            'category_id': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'room_category_name_ru': StringField(),
                    'room_category_name_en': StringField(),

                }
            ),
            'characteristics_id': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'name_ru': StringField(),
                    'name_en': StringField(),
                    'capacity': fields.IntegerField()

                }
            ),
            'child_capacity': fields.IntegerField()
        }
    )
    additional_service_id = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'name_ru': StringField(),
            'name_en': StringField(),
            'price': fields.IntegerField(),
            'currency': StringField()
        }
    )
    child_service_id = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'name_ru': StringField(),
            'name_en': StringField(),
            'until_age': fields.IntegerField(),
            'price': fields.IntegerField(),
            'currency': StringField()
        }
    )
    images = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'image_url': fields.TextField(analyzer=html_strip,
                                      fields={'raw': fields.KeywordField()})
    })
    total = fields.IntegerField()
    hotel_name_ru = TextField()
    hotel_name_en = TextField()
    hotel_address_ru = TextField()
    hotel_address_en = TextField()
    hotel_description_ru = TextField()
    hotel_description_en = TextField()

    class Index:
        name = 'hotels'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Hotel
        fields = [
            'checkin_date',
            'checkout_date',
        ]
        related_models = [HotelImage]

    def get_instances_from_related(self, related_instance):
        return related_instance.hotel


@registry.register_document
class BookingDocument(Document):
    id = fields.IntegerField()
    guest_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'email': fields.TextField(),
    })
    hotel = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'hotel_name_ru': fields.TextField(),
        'hotel_name_en': fields.TextField(),
        'hotel_address_ru': fields.TextField(),
        'hotel_address_en': fields.TextField(),
        'hotel_description_ru': fields.TextField(),
        'hotel_description_en': fields.TextField(),
        'city': fields.ObjectField(
                properties={
                    'city_name_ru': StringField(),
                    'city_name_en': StringField(),
                    'country_id': fields.ObjectField(
                        properties={
                            'country_name_ru': StringField(),
                            'country_name_en': StringField(),
                        }
                    )
                }
            ),
        'food_category': fields.ObjectField(
            properties={
                'food_category_name_ru': fields.TextField(),
                'food_category_name_en': fields.TextField(),
            }
        ),
        'hotel_category': fields.ObjectField(
            properties={
                'hotel_category_name_ru': StringField(),
                'hotel_category_name_en': StringField(),
                'hotel_category_stars': fields.IntegerField()
            }
        ),
        'category_id': fields.ObjectField(
            properties={
                'id': fields.IntegerField(),
                'hotel_category_name_ru': fields.TextField(),
                'hotel_category_name_en': fields.TextField(),
            }
        ),
        'is_active': fields.TextField(),
        'room_id': fields.ObjectField(
                properties={
                    'room_name_ru': StringField(),
                    'room_name_en': StringField(),
                    'room_description_ru': fields.TextField(),
                    'room_description_en': fields.TextField(),
                    'price': fields.IntegerField(),
                    'category_id': fields.ObjectField(
                        properties={
                            'room_category_name_ru': StringField(),
                            'room_category_name_en': StringField(),

                        }
                    ),
                    'characteristics_id': fields.ObjectField(
                        properties={
                            'name_ru': StringField(),
                            'name_en': StringField(),
                            'capacity': fields.IntegerField()

                        }
                    )
                }
            )

    })

    room = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'room_name_ru': fields.TextField(),
        'room_name_en': fields.TextField(),
        'room_description_ru': fields.TextField(),
        'room_description_en': fields.TextField(),
        'price': fields.FloatField(),
        'category_id': fields.ObjectField(
                properties={
                    'room_category_name_ru': StringField(),
                    'room_category_name_en': StringField(),

                }
            ),
        'characteristics_id': fields.ObjectField(
            properties={
                'name_ru': StringField(),
                'name_en': StringField(),
                'capacity': fields.IntegerField()

            }
        )
    })

    class Index:
        name = 'bookings'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Booking
        fields = [
            'checkin_date',
            'checkout_date',
            'num_of_guest'
        ]

