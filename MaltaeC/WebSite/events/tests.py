import os
import io
import datetime

from PIL import Image
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .models import Event, EventType, EventParticipation, EventImages
from .views import all_events_view, remove_event, create_event
from .forms import EventForm
from WebSite.utilizadores.models import Utilizador

#Criacao de dados de teste
class EventTestCase(TestCase):
    #Criacao de dados de teste
    #NOTA: Correr o seguinte no mysql para permitir construcao e edicao da base de dados de teste
    #> GRANT ALL PRIVILEGES ON test_MaltaC.* TO mysqlDBUser@localhost;
    def setUp(self):
        self.factory = RequestFactory()
        event_workshop = EventType(event_name='Workshop')
        event_oficina = EventType(event_name='Oficina')
        event_workshop.save()
        event_oficina.save()
    #Teste get da lista de eventos
    def test_list_events_anon(self):
        request = self.factory.get('/eventos/')
        request.user = AnonymousUser()
        response = all_events_view(request)
        self.assertEqual(response.status_code, 200)
    #Testar insercao de eventos
    def test_insert_event(self):
        photo_file = self.generate_photo_file()
        #TODO update para imagens
        user = Utilizador(email='a@a.com',name='a',phoneNumber='1',type='a',adress='a')
        user.save()
        post_request = self.factory.post('/eventos/agendar/', {'local': 'rua', 'name': 'Teste', 'date_initial': '2016-12-19T16:53',
                                                            'date_final': '2016-12-20T16:53', 'about': 'Descricao do evento',
                                                            'max_participants': '10', 'type': 'Oficina', 'latitude' : '20.0',
                                                           'longitude' : '20.0', 'listTutor':'tut1;tut2;', 'image1':photo_file},
                                                           HTTP_REFERER='/eventos/agendar/')
        post_request.user = user
        response = create_event(post_request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(list(Event.objects.all())),1)
    def test_remove_event(self):
        photo_file = self.generate_photo_file()
        user = Utilizador(email='a@a.com',name='a',phoneNumber='1',type='a',adress='a')
        user.save()
        #TODO update para imagens
        post_insert = self.factory.post('/eventos/agendar/', {'local': 'rua', 'name': 'Teste', 'date_initial': '2016-12-19T16:53',
                                                            'date_final': '2016-12-20T16:53', 'about': 'Descricao do evento',
                                                           'listTutor': 'T1;T3;', 'max_participants': '10', 'type': '1','latitude' : '20.0',
                                                           'longitude' : '20.0','image1':photo_file},
                                                           HTTP_REFERER='/eventos/agendar/')
        post_insert.user = user
        event = EventForm(post_insert.POST, post_insert.FILES)
        self.assertEqual(event.is_valid(), True)
        data = event.cleaned_data
        event_image = EventImages(image1=data['image1'])
        event_image.save()
        event_delete = Event(local=data["local"], name=data["name"], date_initial=data["date_initial"],
                      date_final=data["date_final"], about=data["about"], max_participants=data["max_participants"], images=event_image)
        event_delete.creator = user
        event_delete.save()
        old_size = len(list(Event.objects.all()))
        pk = event_delete.id
        request = self.factory.get('/eventos/remover/'+str(pk))
        response = remove_event(request, pk)
        new_size = len(list(Event.objects.all()))
        self.assertEqual(new_size, old_size-1)

    #Metodo para gerar uma imagem de teste automaticamente
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(410, 410), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
