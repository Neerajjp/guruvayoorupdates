from main.functions import get_current_role
from general.models import ShopDetails


def main_context(request):
    shop_details = ''
    try:
        shop_details = ShopDetails.objects.filter(is_deleted=False)[0]
    except:
        pass
    current_role = get_current_role(request)

    return {
        "shop_details" : shop_details,
    }