import unittest
from datetime import datetime

from mercadona.product import Product
from mercadona.ticket import Ticket
from mercadona.ticket_parser.parser import build_non_vegetable_product, build_ticket, build_vegetable_product, \
    get_bought_at, \
    get_raw_product_list, \
    product_parser, read_pdf_text


class ParserTestCase(unittest.TestCase):
    def test_given_ticket_pdf_when_building_ticket_then_it_is_built_correctly(self):
        ticket = '../tickets/short_ticket.pdf'

        ticket = build_ticket(ticket)

        expected_ticket = Ticket(datetime(2024, 1, 4, 18, 50), [
            Product('MANGO LIMPIACRISTAL', 1, 2.60),
            Product('DISUELVEMANCHAS', 1, 2.0)
        ])
        self.assertEqual(expected_ticket, ticket)

    def test_given_raw_products_when_parsing_product_list_then_it_is_correctly_parsed(self):
        raw_products = [
            '1MANGO LIMPIACRISTAL 2,60',
            '1DISUELVEMANCHAS 2,00',
            '1LIMON',
            '0,180 kg 1,89 €/kg 0,34'
        ]

        products = product_parser(raw_products)

        expected_products = [
            Product('MANGO LIMPIACRISTAL', 1, 2.60),
            Product('DISUELVEMANCHAS', 1, 2.0),
            Product('LIMON', 1, 0.34)
        ]
        self.assertEqual(expected_products, products)

    def test_given_ticket_when_getting_the_product_list_then_it_is_read_correctly(self):
        ticket = '../tickets/short_ticket.pdf'
        raw_ticket_contents = read_pdf_text(ticket)

        product_list = get_raw_product_list(raw_ticket_contents)

        expected_products = [
            '1MANGO LIMPIACRISTAL 2,60',
            '1DISUELVEMANCHAS 2,00'
        ]
        self.assertEqual(expected_products, product_list)

    def test_given_raw_product_when_building_product_then_it_is_built_correctly(self):
        raw_product = '1MANGO LIMPIACRISTAL 2,60'

        product = build_non_vegetable_product(raw_product)

        expected_product = Product('MANGO LIMPIACRISTAL', 1, 2.60)
        self.assertEqual(expected_product, product)

    def test_given_raw_product_with_more_than_1_quantity_when_building_product_then_it_is_built_correctly(self):
        raw_product = '2ALUBIA BLANCA COCIDA 0,69 1,38'

        product = build_non_vegetable_product(raw_product)

        expected_product = Product('ALUBIA BLANCA COCIDA', 2, 1.38)
        self.assertEqual(expected_product, product)

    def test_given_raw_vegetable_product_when_building_product_then_it_is_built_correctly(self):
        raw_product = ['1LIMON', '0,180 kg 1,89 €/kg 0,34']

        product = build_vegetable_product(raw_product[0], raw_product[1])

        expected_product = Product('LIMON', 1, 0.34)
        self.assertEqual(expected_product, product)

    def test_given_raw_ticket_when_getting_the_bought_at_then_it_is_read_correctly(self):
        ticket = '../tickets/short_ticket.pdf'
        raw_ticket_contents = read_pdf_text(ticket)

        bought_at = get_bought_at(raw_ticket_contents)

        expected_bought_at = datetime(2024, 1, 4, 18, 50)
        self.assertEqual(expected_bought_at, bought_at)
