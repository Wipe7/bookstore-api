from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from product.models import Category, Product
from .models import Order, OrderItem


class OrderViewSetTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Aventura')
        self.product = Product.objects.create(
            title='O Senhor dos Aneis',
            author='J.R.R. Tolkien',
            price=59.90,
            category=self.category,
            stock=20
        )
        self.order = Order.objects.create(
            customer_name='Ana Lima',
            customer_email='ana@email.com',
            status='pending'
        )

    def test_listar_pedidos(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_criar_pedido(self):
        url = reverse('order-list')
        data = {
            'customer_name': 'Carlos Souza',
            'customer_email': 'carlos@email.com',
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_detalhe_pedido(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Ana Lima')

    def test_atualizar_pedido(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        data = {
            'customer_name': 'Ana Lima',
            'customer_email': 'ana@email.com',
            'status': 'processing'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'processing')

    def test_deletar_pedido(self):
        url = reverse('order-detail', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_adicionar_item_ao_pedido(self):
        url = reverse('order-add-item', kwargs={'pk': self.order.pk})
        data = {
            'product': self.product.id,
            'quantity': 2,
            'price': '59.90'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_atualizar_status_do_pedido(self):
        url = reverse('order-update-status', kwargs={'pk': self.order.pk})
        response = self.client.patch(url, {'status': 'shipped'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'shipped')

    def test_status_invalido_retorna_erro(self):
        url = reverse('order-update-status', kwargs={'pk': self.order.pk})
        response = self.client.patch(url, {'status': 'invalido'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
