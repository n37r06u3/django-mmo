from django.shortcuts import render_to_response, get_object_or_404

from models import *

def itemtype_list(request):
    
    if request.POST:
        name = request.POST["name"]
        description = request.POST["description"]
        itemtype = ItemType(name=name, description=description)
        itemtype.save()
    
    itemtype_list = ItemType.objects.all()
    
    return render_to_response("items/itemtype_list.html", {
        "itemtype_list": itemtype_list,
    })


def itemtype_detail(request, itemtype_id):
    itemtype = get_object_or_404(ItemType, id=itemtype_id)
    
    if request.POST:
        pass # @@@ for now

    return render_to_response("items/itemtype_detail.html", {
        "itemtype": itemtype,
    })