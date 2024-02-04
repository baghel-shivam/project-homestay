from owner.models import OwnerDetails

def owner_details(request):
    gloabl_details = OwnerDetails.objects.last()
    return {'gloabl_details':gloabl_details}