# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorBriefSerializer, SensorDetailSerializer


class SensorView(APIView):
    def get(self, request, pk=0):
        if pk:
            sensor = Sensor.objects.filter(pk=pk)[0]
            ser = SensorDetailSerializer(sensor)
        else:
            sensors = Sensor.objects.all()
            ser = SensorBriefSerializer(sensors, many=True)
        return Response(ser.data)

    def post(self, request):
        data = request.data
        Sensor(name=data.get('name'), description=data.get('description')).save()
        return Response({'status': 'OK'})

    def patch(self, request, pk):
        sensor = Sensor.objects.filter(pk=pk)[0]
        if 'name' in request.data:
            sensor.name = request.data['name']
        if 'description' in request.data:
            sensor.description = request.data['description']
        sensor.save()
        return Response({'status': 'OK'})


class MeasurementView(APIView):
    def post(self, request):
        data = request.data
        Measurement(sensor_id=data.get('sensor'), temperature=data.get('temperature')).save()
        return Response({'status': 'OK'})
