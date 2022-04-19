from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from authe.models import User
from .models.hotel_models import Hotel, Room
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

    class Django:
        model = Category
        fields = [
            'name',
        ]


@registry.register_document
class FacilitiesAndServicesHotelsDocument(Document):
    class Index:
        name = 'facilities_hotels'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = FacilitiesAndServicesHotels
        fields = [
            'hotel_category_name',
        ]


@registry.register_document
class FacilitiesAndServicesRoomsDocument(Document):
    class Index:
        name = 'facilities_rooms'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = FacilitiesAndServicesRooms
        fields = [
            'room_category_name',
        ]


@registry.register_document
class FoodCategoryDocument(Document):
    class Index:
        name = 'food_category_rooms'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = FoodCategory
        fields = [
            'food_category_name',
            'food_category_abbreviation'
        ]


@registry.register_document
class HotelCategoryStarsDocument(Document):
    class Index:
        name = 'hotel_category_stars'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = HotelCategoryStars
        fields = [
            'hotel_category_name',
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

    class Django:
        model = Country
        fields = [
            'country_name',
        ]


@registry.register_document
class CityDocument(Document):
    country_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'country_name': fields.TextField()
    })

    class Index:
        name = 'city'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = City
        fields = [
            'city_name',
            'postal_code',
        ]


@registry.register_document
class CharacteristicsDocument(Document):
    class Index:
        name = 'characteristics'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Characteristics
        fields = [
            'name',
            'capacity',
        ]


@registry.register_document
class RoomDocument(Document):
    category_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'room_category_name': fields.TextField(),
    })
    characteristics_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'capacity': fields.IntegerField(),
    })

    class Index:
        name = 'room'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Room
        fields = [
            'room_name',
            'room_no',
            'room_description',
            'price'
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
class HotelDocument(Document):
    city = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'city_name': StringField(fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }),
            'country_id': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'country_name': StringField(fields={
                        'raw': KeywordField(),
                        'suggest': fields.CompletionField(),
                }),
                }
            )
        }
    )
    food_category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'food_category_name': fields.TextField(),
        'food_category_abbreviation': fields.TextField(),
    })
    hotel_category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'hotel_category_name': fields.TextField(),
        'hotel_category_stars': fields.TextField(),
    })
    category_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'hotel_category_name': fields.TextField(),
    })
    room_id = fields.ObjectField(
        properties={
            'id': fields.IntegerField(),
            'room_name': StringField(),
            'room_no': fields.IntegerField(),
            'room_description': fields.TextField(),
            'price': fields.IntegerField(),
            'category_id': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'room_category_name': StringField(),

                }
            ),
            'characteristics_id': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(),
                    'name': StringField(),
                    'capacity': fields.IntegerField()

                }
            )
        }
    )

    class Index:
        name = 'hotels'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Hotel
        fields = [
            'hotel_name',
            'hotel_address',
            'hotel_description',
        ]


@registry.register_document
class BookingDocument(Document):
    id = fields.IntegerField()
    guest_id = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'email': fields.TextField(),
    })
    hotel = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'hotel_name': fields.TextField(),
        'hotel_address': fields.TextField(),
        'hotel_description': fields.TextField(),
        'city': fields.ObjectField(
                properties={
                    'city_name': StringField(),
                    'country_id': fields.ObjectField(
                        properties={
                            'country_name': StringField(),
                        }
                    )
                }
            ),
        'food_category': fields.ObjectField(
            properties={
                'food_category_name': fields.TextField(),
                'food_category_abbreviation': fields.TextField()
            }
        ),
        'hotel_category': fields.ObjectField(
            properties={
                'hotel_category_name': StringField(),
                'hotel_category_stars': fields.IntegerField()
            }
        ),
        'category_id': fields.ObjectField(
            properties={
                'id': fields.IntegerField(),
                'hotel_category_name': fields.TextField(),
            }
        ),
        'is_active': fields.TextField(),
        'room_id': fields.ObjectField(
                properties={
                    'room_name': StringField(),
                    'room_no': fields.IntegerField(),
                    'room_description': fields.TextField(),
                    'price': fields.IntegerField(),
                    'category_id': fields.ObjectField(
                        properties={
                            'room_category_name': StringField(),

                        }
                    ),
                    'characteristics_id': fields.ObjectField(
                        properties={
                            'name': StringField(),
                            'capacity': fields.IntegerField()

                        }
                    )
                }
            )

    })

    room = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'room_name': fields.TextField(),
        'room_no': fields.IntegerField(),
        'room_description': fields.TextField(),
        'price': fields.FloatField(),
        'category_id': fields.ObjectField(
                properties={
                    'room_category_name': StringField(),

                }
            ),
        'characteristics_id': fields.ObjectField(
            properties={
                'name': StringField(),
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

