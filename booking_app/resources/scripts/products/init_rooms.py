from reservations.models import Room

def create_rooms() -> None:
    room: dict[str, list[int]] = {
        'rooms': [31, 32, 33, 34]
    }

    rooms_to_create = [
        Room(name='Room', number=num, max_amount_of_people=5)
        for room_type, room_numbers in room.items()
        for num in room_numbers
    ]

    Room.objects.bulk_create(rooms_to_create)