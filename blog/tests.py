from django.test import TestCase
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_trump= User.objects.create_user(
            username='trump',
            password='somepassword'
        )
        self.user_obama = User.objects.create_user(
            username='obama',
            password='somepassword'
        )

    def navbar_test(self, soup):
        navbar = soup.nav


        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        #<a> 텍스트가 '스마트 부산'인 href가 '/' 와 동일한지
        logo_btn = navbar.find('a', text ='스마트 부산')
        self.assertIn(logo_btn.attrs['href'],'/')

        home_btn = navbar.find('a', text='Home')
        self.assertIn(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text ='Blog')
        self.assertIn(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text ='About Me')
        self.assertIn(about_me_btn.attrs['href'], '/about_me/')


    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog') #페이지의 타이틀에 Blog라는 문구가 포함되어 있는가

        self.navbar_test(soup)#위에서 선언한 navbar 호출


        self.assertEqual(Post.objects.count(),0)
        main_area=soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        post_001= Post.objects.create(
            title= '첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama
        )
        self.assertEqual(Post.objects.count(), 2)

        response=self.client.get('/blog/')
        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        main_area=soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

    def test_post_detail(self):
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.'

        )
        post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='Hello World. We are the world.'
        )

        self.assertEqual(post_001.get_absoulte_url(), '/blog/1/')

        response = self.client.get(post_001.get_absoulte_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')

        navbar= soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        self.assertIn(post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id= 'post-area')
        self.assertIn(post_001.title, post_area.text)

        self.assertIn(post_001.content, post_area.text)



        # Create your tests here.
