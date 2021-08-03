from django.shortcuts import render
from .models import Order,Project
from .serializers import Orderserializers,Projectserializers
from rest_framework import status
from rest_framework import  viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from googletrans  import Translator
from django.shortcuts import get_object_or_404

def do_translator(text,translated_language):
    trns=[]
    translator=Translator()
    for lang in translated_language:
        translat=translator.translate(text,dest=lang)
        trns.append(translat.text)
    print(trns)
    return trns


class Odervewsets(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = Orderserializers


    @action(detail=True, methods=['GET'])
    def get_queryset(self):
        print('func calling..')
        project = Project.objects.all()
        print(project,"project")
        for data in project:
            id=data.id
            text=data.text
            translated_language=eval(data.translated_to_language)
            print("translated_language", translated_language)
            trans=do_translator(text,translated_language)
            orders=Order.objects.create(project_id=data,translated_tex=trans)
            orders.save()
        return self.queryset


    @action(detail=True, methods=['PATCH'])
    def patch(self, request, pk):
        order=Order.objects.get(id=pk)
        serializer_class=Orderserializers(order,data=request.data,partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors,status=status.HTTP_400_BAD_REQUEST)
class Project_view(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = Projectserializers
    lookup_field = 'pk'

    @action(detail=True, methods=['PUT'])
    def put(self, request, *args, **kwargs):
        project =  Project.objects.all()
        serializer_class = Projectserializers(instance=project, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PATCH'])
    def patch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        project = Project.objects.get(pk=pk)
        serializer_class = Projectserializers(project, data=request.data,partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        project = Project.objects.get(pk=pk)
        project.delete()

    @action(detail=True, methods=['POST'])
    def create(self, request, *args, **kwargs):
        data=request.data
        project=Project.objects.create(id=data['id'],project_name=data['project_name'],text=data['text'],
                                       translated_to_language=data['translated_to_language'],created_at=data['created_at'],updated_at=data['updated_at'])
        project.save()
        serializer=Projectserializers(project,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class Register_view(APIView):
    def get(self, request):
        register = Order.objects.all()
        serializer = Orderserializers(register, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = Orderserializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login_view(APIView):
    authentication_classes = [ BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)