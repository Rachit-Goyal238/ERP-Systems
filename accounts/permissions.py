from django.contrib.auth.decorators import user_passes_test


def is_hr(user):

    return user.groups.filter(
        name='HR'
    ).exists()


def is_inventory_manager(user):

    return user.groups.filter(
        name='Inventory Manager'
    ).exists()


def is_admin(user):

    return user.is_superuser