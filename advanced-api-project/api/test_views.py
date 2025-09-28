from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="other", password="password123")

        # Create authors
        self.author_rowling = Author.objects.create(name="J. K. Rowling")
        self.author_tolkein = Author.objects.create(name="J. R. R. Tolkien")
        self.author_orwell = Author.objects.create(name="George Orwell")

        # Create books (varied titles / years for filtering/search/ordering)
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author_rowling
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author_rowling
        )
        self.book3 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author_tolkein
        )
        self.book4 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author_orwell
        )

        # API client
        self.client = APIClient()

    def test_list_books_returns_metadata_and_results(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # If paginated, response.data should be a dict containing 'results' or 'count'
        self.assertTrue(isinstance(response.data, dict))
        # metadata should be present
        self.assertIn('metadata', response.data)
        # results present
        self.assertIn('results', response.data)
        # ensure correct number of items returned (page default)
        self.assertGreaterEqual(len(response.data['results']), 4)

    def test_filter_by_author_id(self):
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author_rowling.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        titles = {r['title'] for r in results}
        self.assertIn("Harry Potter and the Philosopher's Stone", titles)
        self.assertIn("Harry Potter and the Chamber of Secrets", titles)
        self.assertNotIn("The Hobbit", titles)

    def test_search_by_title_and_author_name(self):
        url = reverse('book-list')
        # search for 'harry' should match the two Rowling books
        response = self.client.get(url, {'search': 'harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertGreaterEqual(len(results), 2)
        for item in results:
            self.assertTrue('harry' in item['title'].lower() or 'rowling' in item.get('author_display', '') or 'rowling' in item.get('author', ''))

        # search by author name 'tolkein' should return 'The Hobbit'
        response2 = self.client.get(url, {'search': 'tolkein'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        titles = [r['title'] for r in response2.data['results']]
        self.assertIn('The Hobbit', titles)

    def test_ordering_by_publication_year_desc(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        years = [item['publication_year'] for item in results]
        # list should be non-increasing
        self.assertTrue(all(years[i] >= years[i+1] for i in range(len(years)-1)))

    def test_retrieve_book_includes_related_books(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # related_books should be present and not include the book itself
        self.assertIn('related_books', response.data)
        related = response.data['related_books']
        # Should include at least one other Rowling book (book2)
        titles = [b['title'] for b in related]
        self.assertIn("Harry Potter and the Chamber of Secrets", titles)
        self.assertNotIn(self.book1.title, titles)

    def test_create_book_requires_authentication(self):
        url = reverse('book-create')

        payload = {
            "title": "A New Test Book",
            "publication_year": 2025,
            "author": self.author_orwell.id
        }

        # Unauthenticated attempt should fail (401 or 403 depending on settings)
        response = self.client.post(url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticate and try again
        self.client.force_authenticate(user=self.user)
        response2 = self.client.post(url, payload, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.data['data']['title'], payload['title'])
        # cleanup authentication
        self.client.force_authenticate(user=None)

    def test_update_book_authenticated(self):
        url = reverse('book-update', kwargs={'pk': self.book4.pk})
        update_payload = {'title': 'Nineteen Eighty-Four'}

        # unauthenticated should fail
        unauth = self.client.patch(url, update_payload, format='json')
        self.assertIn(unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticate
        self.client.force_authenticate(user=self.user)
        resp = self.client.patch(url, update_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['data']['title'], 'Nineteen Eighty-Four')
        # verify DB changed
        self.book4.refresh_from_db()
        self.assertEqual(self.book4.title, 'Nineteen Eighty-Four')
        self.client.force_authenticate(user=None)

    def test_delete_book_authenticated(self):
        url = reverse('book-delete', kwargs={'pk': self.book3.pk})

        # unauthenticated delete attempt
        unauth = self.client.delete(url)
        self.assertIn(unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticate
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # record should be deleted
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book3.pk)
        self.client.force_authenticate(user=None)

    def test_author_list_and_detail_metadata_and_statistics(self):
        list_url = reverse('author-list')
        resp = self.client.get(list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('metadata', resp.data)

        detail_url = reverse('author-detail', kwargs={'pk': self.author_rowling.pk})
        resp2 = self.client.get(detail_url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        # statistics should be present on author detail
        self.assertIn('statistics', resp2.data)
        stats = resp2.data['statistics']
        self.assertIn('total_books', stats)
        self.assertGreaterEqual(stats['total_books'], 2)
