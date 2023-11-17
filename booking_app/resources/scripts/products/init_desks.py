from reservations.models import Desk


def create_desks() -> None:
    desk_types: dict[str, list[int]] = {
    'narrows_desks': [1, 2, 3, 4, 18, 19, 20, 21, 22, 23],
    'large_desks': [5, 12, 13, 14, 15, 16, 17, 24, 25, 29, 30],
    'small_desks':  [6, 7, 8, 9, 10, 11, 26, 27, 28]
    }

    desks_to_create = [
        Desk(name='Desk', type=desk_type, number=num)
        for desk_type, desk_numbers in desk_types.items()
        for num in desk_numbers
    ]


    Desk.objects.bulk_create(desks_to_create)


