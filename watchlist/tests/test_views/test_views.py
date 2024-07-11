from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist.models import StreamPlatform, WatchList, Review


class StreamPlatformViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpassword')
        # self.admin = User.objects.create_superuser(username='admin', password='adminpassword')
        # self.client.login(username='testuser', password='testpassword')
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name='Netflix',
                                                    about='Best Platform',
                                                    website='https://netflix.com')

    # login as a user not an admin
    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "Best Platform",
            "website": "https://netflix.com"
        }
        # we test routers by using reverse
        # the name of view is streamplatform-modelviewset
        # we need to add -list or -detail to the name of the view
        # and if i added the appname, it will be like this: appname:viewname
        reverse_url = reverse("watchlist:streamplatform-modelviewset-list")

        # the permissons classes is permission_classes = [AdminOrReadOnly]
        # we need to login as an admin to create a stream platform
        response = self.client.post(reverse_url, data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    # user can make a get request
    def test_streamplatform_list(self):
        reverse_url = reverse("watchlist:streamplatform-modelviewset-list")
        response = self.client.get(reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_streamplatform_list_indvidual_element(self):
        reverse_url = reverse("watchlist:streamplatform-modelviewset-detail", args=(self.stream.id,))
        response = self.client.get(reverse_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Netflix')


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name='Netflix',
                                                    about='Best Platform',
                                                    website='https://netflix.com')
        self.watchlist = WatchList.objects.create(platform=self.stream,
                                                  title='Example Movie',
                                                  storyline='Example Storyline',
                                                  active=True)

    def test_watchlist_create(self):
        data = {
            "platform": self.stream.id,
            "title": "Example Movie",
            "storyline": "Example Storyline",
            "active": True
        }
        reverse_url = reverse("watchlist:watchlist-list")
        response = self.client.post(reverse_url, data)
        self.assertEqual(response.status_code, 403)

    def test_watchlist_list(self):
        reverse_url = reverse("watchlist:watchlist-list")
        response = self.client.get(reverse_url)
        self.assertEqual(response.status_code, 200)

    def test_watchlist_indvidual_element(self):
        reverse_url = reverse("watchlist:watchlist-detail", args=(self.watchlist.id,))
        response = self.client.get(reverse_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Example Movie')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpassword')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = StreamPlatform.objects.create(name='Netflix',
                                                    about='Best Platform',
                                                    website='https://netflix.com')
        self.watchlist = WatchList.objects.create(platform=self.stream,
                                                  title='Example Movie',
                                                  storyline='Example Storyline',
                                                  active=True)
        self.watchlist2 = WatchList.objects.create(platform=self.stream,
                                                   title='Example Movie 2',
                                                   storyline='Example Storyline 2',
                                                   active=True)
        # Passing ids instead of objects ensures that
        # the data structure aligns with the expectations of the serializers
        # and views, avoiding validation errors and ensuring smooth data processing.
        # This is why the ids are passed in the data dictionary in your test cases.

        self.review = Review.objects.create(reviewer=self.user,
                                            watchlist=self.watchlist2,
                                            rating=5,
                                            review="Example Review")

    def test_review_create(self):
        data = {
            "reviewer": self.user.id,
            "watchlist": self.watchlist.id,
            "rating": 5,
            "review": "Example Review"
        }
        reverse_url = reverse("watchlist:review-create", args=(self.watchlist.id,))
        response = self.client.post(reverse_url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        # the get not valid now because the review is not the first one, we have a multiple reviews objects
        # self.assertEqual(Review.objects.get().rating, 5)
        # not allowed twice review for the same user
        response = self.client.post(reverse_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Review.objects.count(), 2)

    def test_review_create_unauth(self):
        data = {
            "reviewer": self.user.id,
            "watchlist": self.watchlist.id,
            "rating": 5,
            "review": "Example Review",
            "active": True
        }
        self.client.force_authenticate(user=None)
        reverse_url = reverse("watchlist:review-create", args=(self.watchlist.id,))
        response = self.client.post(reverse_url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        admin_user = User.objects.create_user(username='admin_user', password='testpassword', is_staff=True,
                                              is_superuser=True)
        admin_token, _ = Token.objects.get_or_create(user=admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + admin_token.key)

        data = {
            "reviewer": admin_user.id,
            "watchlist": self.watchlist.id,
            "rating": 4,
            "review": "Updated Review",
            "active": False
        }
        # we need to force authenticate the user
        # because the review is created by admin or staff
        reverse_url = reverse("watchlist:review-detail", args=(self.review.id,))
        response = self.client.put(reverse_url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_review_list(self):
        reverse_url = reverse("watchlist:review-list")
        response = self.client.get(reverse_url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_review_indvidual_element(self):
        reverse_url = reverse("watchlist:review-detail", args=(self.review.id,))
        response = self.client.get(reverse_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['rating'], 5)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, 200)
