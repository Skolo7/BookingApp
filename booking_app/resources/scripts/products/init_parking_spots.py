from reservations.models import Parking


def create_parking_spots() -> None:
    parking_spots: dict[str, list[int]] = {
        'parking_places': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    }

    parking_spots_to_create = [
        Parking(number=num)
        for parking_type, parking_numbers in parking_spots.items()
        for num in parking_numbers
    ]

    Parking.objects.bulk_create(parking_spots_to_create)
