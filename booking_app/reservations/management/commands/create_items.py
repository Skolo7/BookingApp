from django.core.management.base import BaseCommand, CommandError
from reservations.models import Desk, Parking, Room
from typing import Any, TypeVar


T = TypeVar('T', Desk, Parking, Room)



class ItemCreator:
    @staticmethod
    def create_items(model_class: type[T], items_data: list[dict[str, Any]]) -> None:
        items = [
            model_class(**item_data)
            for item_data in items_data
        ]
        model_class.objects.bulk_create(items)

class Command(BaseCommand):
    ROOM_DATA = [
        {'name': 'Room', 'number': 31, 'max_amount_of_people': 5, 'type': 'blue_room'},
        {'name': 'Room', 'number': 32, 'max_amount_of_people': 5, 'type': 'green_room'},
        {'name': 'Room', 'number': 33, 'max_amount_of_people': 5, 'type': 'yellow_room'},
        {'name': 'Room', 'number': 34, 'max_amount_of_people': 5, 'type': 'red_room'},
    ]

    PARKING_DATA = [
        {'number': num} for num in range(1, 15)
    ]

    DESK_DATA = [
        {'name': 'Desk', 'type': 'narrows_desks', 'number': num}
        for num in [1, 2, 3, 4, 18, 19, 20, 21, 22, 23]
    ] + [
        {'name': 'Desk', 'type': 'large_desks', 'number': num}
        for num in [5, 12, 13, 14, 15, 16, 17, 24, 25, 29, 30]
    ] + [
        {'name': 'Desk', 'type': 'small_desks', 'number': num}
        for num in [6, 7, 8, 9, 10, 11, 26, 27, 28]
    ]

    def handle(self, *args: Any, **options: Any) -> None:
        creator = ItemCreator()
        
        creator.create_items(Room, self.ROOM_DATA)
        creator.create_items(Parking, self.PARKING_DATA)
        creator.create_items(Desk, self.DESK_DATA)

        self.stdout.write(self.style.SUCCESS('Successfully created items'))