from django.shortcuts import render
from .models import Containers, Position
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def bengal_current(current_position, drift_speed):
    lat, lon = current_position
    new_lat = lat + drift_speed
    new_position = (new_lat, lon)
    return new_position

def index(request):
    containers = Containers.objects.all()
    return render(request, 'index.html', {'containers':containers})

def map(request):
    positions = Position.objects.all()    
    context = {'positions': positions}
    return render(request, 'map.html', context)

def get_positions(request):
    if request.method == "GET":
        positions = Position.objects.all()
        positions_data = [
            {'id': position.id, 'latitude': position.latitude, 'longitude': position.longitude, 'steps_left': position.steps_left, 'currentname': position.currentname} for position in positions
        ]
        return JsonResponse({'positions': positions_data})
    return JsonResponse({'message': 'Invalid request method'})


from django.db.models import F


@csrf_exempt
def update_positions_northpacific(request):
    if request.method == 'GET':
        position_id = request.GET.get('position_id')
        try:
            position = Position.objects.get(id=position_id) # Get position by id

            if position:
                position.latitude = F('latitude') + 1
                position.longitude = F('longitude') + 0.5
                position.steps_left = F('steps_left') - 1
                position.save()

                response_data = {'message': 'Position updated successfully'}
            else:
                response_data = {'message': 'No positions found'}

        except Exception as e:
            response_data = {'message': 'Error updating positions: ' + str(e)}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def update_positions_californian(request):
    if request.method == 'GET':
        position_id = request.GET.get('position_id')
        try:
            position = Position.objects.get(id=position_id) # Get position by id

            if position:
                position.latitude = F('latitude') - 1
                position.longitude = F('longitude') + 0.5
                position.steps_left = F('steps_left') - 1
                position.save()

                response_data = {'message': 'Position updated successfully'}
            else:
                response_data = {'message': 'No positions found'}

        except Exception as e:
            response_data = {'message': 'Error updating positions: ' + str(e)}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def update_positions_canaries(request):
    if request.method == 'GET':
        position_id = request.GET.get('position_id')
        try:
            position = Position.objects.get(id=position_id) # Get position by id

            if position:
                position.latitude = F('latitude') - 1
                position.longitude = F('longitude') - 0.5
                position.steps_left = F('steps_left') - 1
                position.save()

                response_data = {'message': 'Position updated successfully'}
            else:
                response_data = {'message': 'No positions found'}

        except Exception as e:
            response_data = {'message': 'Error updating positions: ' + str(e)}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def update_positions_gulfstream(request):
    if request.method == 'GET':
        position_id = request.GET.get('position_id')
        try:
            position = Position.objects.get(id=position_id)
            
            if position:
                if position.currentname == "canaries":
                    position.currentname = "gulfstream"
                position.latitude = F('latitude') + 0.6
                position.longitude = F('longitude') - 1
                position.steps_left = F('steps_left') - 1
                position.save()

                response_data = {'message': 'Position updated successfully'}
            else:
                response_data = {'message': 'No positions found'}

        except Exception as e:
            response_data = {'message': 'Error updating positions: ' + str(e)}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def update_positions_northpacific(request):
    if request.method == 'GET':
        position_id = request.GET.get('position_id')
        try:
            position = Position.objects.get(id=position_id) # Get position by id

            if position:
                position.latitude = F('latitude') + 0.3
                position.longitude = F('longitude') + 1
                position.steps_left = F('steps_left') - 1
                position.save()

                response_data = {'message': 'Position updated successfully'}
            else:
                response_data = {'message': 'No positions found'}

        except Exception as e:
            response_data = {'message': 'Error updating positions: ' + str(e)}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def update_positions_westwinddrift(request):
    if request.method == 'GET':
        position_id = request.GET.get('position_id')
        try:
            position = Position.objects.get(id=position_id) # Get position by id

            if position:
                position.longitude = F('longitude') + 1
                position.steps_left = F('steps_left') - 1
                position.save()

                response_data = {'message': 'Position updated successfully'}
            else:
                response_data = {'message': 'No positions found'}

        except Exception as e:
            response_data = {'message': 'Error updating positions: ' + str(e)}

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method'})
# @csrf_exempt
# def update_positions(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data)
#             latitude = data.get('latitude')
#             longitude = data.get('longitude')
#             position = Position.objects.order_by('id').first()
#             if position:
#                 position.latitude = latitude
#                 position.longitude = longitude
#                 position.save()

#                 response_data = {'message': 'Position updated successfully'}
#             else:
#                 response_data = {'message': 'No positions found'}

#         except Exception as e:
#             response_data = {'message': 'Error updating positions: ' + str(e)}

#         return JsonResponse(response_data)

#     return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def add_position(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if latitude and longitude:
            steps_left = 20
            if data.get('currentname'):
                currentname = data.get('currentname')
                if currentname == "canaries":
                    steps_left = 50
                elif currentname == "northpacific":
                    steps_left = 29
                elif currentname == "westwinddrift":
                    steps_left = 50
            else:
                currentname = 'bengalcurrent'
        Position.objects.create(latitude=latitude, longitude=longitude, currentname=currentname, steps_left=steps_left)
        return JsonResponse({'message': 'Position added successfully'})
    return JsonResponse({'message': 'Invalid request method'})



