from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Category, Product


class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Ficção Científica',
            description='Livros de ficção científica'
        )

    def test_listar_categorias(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_criar_categoria(self):
        url = reverse('category-list')
        data = {'name': 'Romance', 'description': 'Livros romanticos'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Romance')

    def test_detalhe_categoria(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Ficção Científica')

    def test_atualizar_categoria(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        data = {'name': 'Fantasia', 'description': 'Livros de fantasia'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Fantasia')

    def test_deletar_categoria(self):
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class ProductViewSetTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Terror')
        self.product = Product.objects.create(
            title='It - A Coisa',
            author='Stephen King',
            price=45.00,
            category=self.category,
            stock=5
        )

    def test_listar_produtos(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_criar_produto(self):
        url = reverse('product-list')
        data = {
            'title': 'O Iluminado',
            'author': 'Stephen King',
            'price': '39.90',
            'category': self.category.id,
            'stock': 8
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_detalhe_produto(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'It - A Coisa')

    def test_atualizar_produto(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'title': 'It - A Coisa',
            'author': 'Stephen King',
            'price': '55.00',
            'category': self.category.id,
            'stock': 10
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 10)

    def test_deletar_produto(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_filtrar_produto_por_categoria(self):
        url = reverse('product-list')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
