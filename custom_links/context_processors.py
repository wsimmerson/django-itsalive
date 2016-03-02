from .models import Link


def custom_link_processor(request):
    custom_links = Link.objects.extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')
    return {'custom_links': custom_links}
