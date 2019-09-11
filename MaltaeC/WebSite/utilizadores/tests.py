from django.test import TestCase, RequestFactory
from .models import BaseUser, Artesao, Criativo, Utilizador, PropostaRegisto
from .views import viewProfile, register, loginView, edit_profile_action, logoutView
from django.conf import settings
from importlib import import_module
from django.contrib.auth.models import AnonymousUser

#Criacao de dados de teste
class EventTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        proposta1 = PropostaRegisto(texto="aaa", imgUrl="imgurl", videoUrl="videourl")
        proposta1.save()
        artesao = Artesao(email="artesao@email.com", password="pass",name = "testeArtesao", geolocation = "geolocation" ,latitude = "0.0",longitude ="0.0",phoneNumber ="91",type = "artesao",is_active= False, propostaRegisto=proposta1)
        artesao.set_password("pass")
        artesao.is_active=True
        artesao.save()

        proposta2 = PropostaRegisto(texto="bbb",imgUrl="imgurl2",videoUrl="videourl2")
        proposta2.save()
        userCriativo = Criativo(email="criativo@email.com", password="pass",name = "testeCriativo", geolocation = "geolocation",latitude = "0.0",longitude = "0.0",phoneNumber = "91",type = "criativo",is_active=False, propostaRegisto=proposta2)
        userCriativo.set_password("pass")
        userCriativo.is_active=True
        userCriativo.save()

        userUtilizador = Utilizador(email="utilizador@email.com", password="pass",name = "testUser",phoneNumber = "91",adress = "adress",type="utilizador")
        userUtilizador.set_password("pass")
        userUtilizador.is_active=True
        userUtilizador.save()

    def test_logout(self):
        post_request = self.factory.post('/utilizadores/logout/')
        user = Utilizador.objects.filter(email="utilizador@email.com").get()
        post_request.user = user
        post_request.session = self.client.session
        response = logoutView(post_request)
        self.assertEqual(response.status_code, 302)

    def test_edit_local(self):
        post_request = self.factory.post('/utilizadores/editProfileAction/', {'geolocation': 'Amarante',
                                                                                  'latitude': '3.0',
                                                                                  'longitude': '3.3'
                                                                                  })
        user = Criativo.objects.filter(email="criativo@email.com").get()
        post_request.user = user
        response = edit_profile_action(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_request.user.criativo.geolocation, "Amarante")
        self.assertEqual(post_request.user.criativo.latitude, 3.0)
        self.assertEqual(post_request.user.criativo.longitude, 3.3)

    def test_edit_adress(self):
        post_request = self.factory.post('/utilizadores/editProfileAction/', {'adress': 'testAdress',
                                                                                  })
        user = Utilizador.objects.filter(email="utilizador@email.com").get()
        post_request.user = user
        response = edit_profile_action(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_request.user.utilizador.adress, "testAdress")

    def test_edit_password(self):
        post_request = self.factory.post('/utilizadores/editProfileAction/', {'new_password': 'testPass',
                                                                                  'old_password': 'pass'})
        post_request.session = self.client.session
        user = Utilizador.objects.filter(email="utilizador@email.com").get()
        post_request.user = user
        response = edit_profile_action(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_request.user.check_password("testPass"), True)

    def test_edit_name(self):
        post_request = self.factory.post('/utilizadores/editProfileAction/', {'name': 'newName',
                                                                                  'edit-submit': 'edit-submit'})
        user = Utilizador.objects.filter(email="utilizador@email.com").get()
        post_request.user = user
        response = edit_profile_action(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post_request.user.name, "newName")

    def test_login_artesao(self):
        user = Artesao.objects.filter(email="artesao@email.com").get()
        post_request = self.factory.post('/utilizadores/login/', {'username': 'artesao@email.com',
                                                                      'password': 'pass',
                                                                      'login-submit': 'login-submit'},
                                             HTTP_REFERER='/home/')
        post_request.session = self.client.session
        response = loginView(post_request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.is_authenticated, True)

    def test_login_criativo(self):
        user = Criativo.objects.filter(email="criativo@email.com").get()
        post_request = self.factory.post('/utilizadores/login/', {'username': 'criativo@email.com',
                                                                      'password': 'pass',
                                                                      'login-submit': 'login-submit'},
                                             HTTP_REFERER='/home/')
        post_request.session = self.client.session
        response = loginView(post_request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.is_authenticated, True)

    def test_login_utilizador(self):
        user = Utilizador.objects.filter(email="utilizador@email.com").get()
        post_request = self.factory.post('/utilizadores/login/', {'username': 'utilizador@email.com',
                                                                      'password': 'pass',
                                                                      'login-submit': 'login-submit'},
                                             HTTP_REFERER='/home/')
        post_request.session = self.client.session
        response = loginView(post_request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.is_authenticated, True)

    #Teste registar artesao
    def test_criar_artesao(self):
        post_request = self.factory.post('/utilizadores/registo/',
                                         {'username': 'artesaoTeste',
                                          'email': 'artesao@teste.com',
                                          'password': '123psw',
                                          'password_confirm_maker': '123psw',
                                          'phone_maker': '915522421',
                                          'choiceType': 'artesao',
                                          'geolocation': 'geolocationteste',
                                          'latitude': '0.0',
                                          'longitude': '0.0',
                                          'areatexto': 'texto proposta',
                                          'imgProposta': 'imgProposta',
                                          'videoURL': 'youtube',
                                          'test-envtest': 'test-envtest',
                                          'maker-submit':'maker-submit'},
                                        HTTP_REFERER='/utilizadores/registo/')

        post_request.user = AnonymousUser()

        response = register(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Artesao.objects.filter(email="artesao@teste.com").exists(), True)

    # Teste registar criativo
    def test_criar_criativo(self):
        post_request = self.factory.post('/utilizadores/registo/',
                                         {'username': 'criativoTeste',
                                          'email': 'criativo@teste.com',
                                          'password': '123psw',
                                          'password_confirm_maker': '123psw',
                                          'phone_maker': '915522421',
                                          'choiceType': 'criativo',
                                          'geolocation': 'geolocationteste',
                                          'latitude': '0.0',
                                          'longitude': '0.0',
                                          'areatexto': 'texto proposta',
                                          'imgProposta': 'imgProposta',
                                          'videoURL': 'youtube',
                                          'test-envtest': 'test-envtest',
                                          'maker-submit': 'maker-submit'},
                                         HTTP_REFERER='/utilizadores/registo/')

        post_request.user = AnonymousUser()

        response = register(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Criativo.objects.filter(email="criativo@teste.com").exists(), True)

    # Teste registar regular
    def test_criar_regular(self):
        post_request = self.factory.post('/utilizadores/registo/',
                                         {'username_regular': 'regularTeste',
                                          'email_regular': 'regular@teste.com',
                                          'password_regular': '123psw',
                                          'password_confirm_regular': '123psw',
                                          'phone_regular': '915522421',
                                          'address_regular': 'rua teste',
                                          'regular-submit': 'regular-submit'},
                                         HTTP_REFERER='/utilizadores/registo/')

        post_request.user = AnonymousUser()

        response = register(post_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Utilizador.objects.filter(email="regular@teste.com").exists(), True)



    # Teste ver perfil existente
    def test_ver_perfil_existente(self):
        post_request = self.factory.post('/utilizadores/registo/',
                                         {'username_regular': 'regularTeste',
                                          'email_regular': 'regular@teste.com',
                                          'password_regular': '123psw',
                                          'password_confirm_regular': '123psw',
                                          'phone_regular': '915522421',
                                          'address_regular': 'rua teste',
                                          'regular-submit': 'regular-submit'},
                                         HTTP_REFERER='/utilizadores/registo/')


        post_request.user = AnonymousUser()

        register(post_request)
        self.assertEqual(Utilizador.objects.filter(email="regular@teste.com").exists(), True)
        user = Utilizador.objects.filter(email="regular@teste.com").get()

        #Ver perfil
        urlperfil = "/utilizadores/perfil?id=" + str(user.id)
        get_request = self.factory.get(urlperfil)

        get_request.user = AnonymousUser()

        response = viewProfile(get_request)
        self.assertEqual(response.status_code, 200)



    # Teste ver perfil inexistente
    def test_ver_perfil_inexistente(self):
        get_request = self.factory.get('/utilizadores/perfil?id=999')

        response = viewProfile(get_request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], "/home") #redirecionou para o correto





