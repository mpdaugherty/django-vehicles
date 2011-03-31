import json
from django.http import HttpResponse
from vehicles.models import CarMake, CarModel

def makes_for_year(request, year):
    response = []
    makes = CarMake.objects.filter(carmodel__year__exact=year).distinct().order_by('name')
    for make in makes:
        response.append(make.name)
    return HttpResponse(json.dumps(response), mimetype="application/json")

def models_for_make_and_year(request, make, year):
    response = []
    models = CarModel.objects.filter(make__name__iexact=make, year=year).order_by('name')
    for model in models:
        response.append({'id': model.id, 'name': model.name})
    return HttpResponse(json.dumps(response), mimetype="application/json")
