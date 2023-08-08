from reservations.models import Desk


def create_small_desks():
    narrows_desks = [1, 2, 3, 4, 18, 19, 20, 21, 22, 23]
    large_desks = [5, 12, 13, 14, 15, 16, 17, 24, 25, 29, 30]
    small_desks = [6, 7, 8, 9, 10, 11, 26, 27, 28]

    desks_to_create = []
    for num in narrows_desks:
        desk_instance = Desk(name='Desk', type='narrow_desk', number=num)
        desks_to_create.append(desk_instance)

    for num in large_desks:
        desk_instance = Desk(name='Desk', type='large_desk', number=num)
        desks_to_create.append(desk_instance)

    for num in small_desks:
        desk_instance = Desk(name='Desk', type='small_desk', number=num)
        desks_to_create.append(desk_instance)


    Desk.objects.bulk_create(desks_to_create)