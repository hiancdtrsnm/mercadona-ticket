import re
from datetime import datetime
from typing import IO, Union, Any

from pypdf import PdfReader

from mercadona.product import Product
from mercadona.ticket import Ticket


def build_ticket(path: Union[str, IO[Any]]) -> Ticket:
    """
    Builds a Ticket object from a PDF file
    The PDF file must be a ticket from Mercadona
    This function can be used to parse a ticket from a file in the filesystem or from a BytesIO object
    """
    raw_ticket_contents = read_pdf_text(path)
    bought_at = get_bought_at(raw_ticket_contents)
    products = build_product_list(raw_ticket_contents)
    return Ticket(bought_at=bought_at, products=products)


def read_pdf_text(path: Union[str, IO[Any]]) -> str:
    reader = PdfReader(path)
    content = []
    for page in reader.pages:
        content.append(page.extract_text())
    return "\n".join(content)


def get_bought_at(raw_ticket: str) -> datetime:
    regex = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"
    bought_at_str = re.search(regex, raw_ticket)[0]
    return datetime.strptime(bought_at_str, "%d/%m/%Y %H:%M")


def build_product_list(raw_ticket: str) -> list[Product]:
    raw_product_list = get_raw_product_list(raw_ticket)
    return product_parser(raw_product_list)


def get_raw_product_list(raw_ticket: str) -> list[str]:
    return find_product_list_lines(raw_ticket.split("\n"))


def find_product_list_lines(lines: list[str]) -> list[str]:
    start_index = index(lines, lambda line: "Descripción" in line)
    end_index = index(lines, lambda line: "TOTAL" in line)
    return lines[start_index + 1 : end_index]


def index(l, f):
    return next((i for i in range(len(l)) if f(l[i])), None)


def product_parser(raw_products: list[str]) -> list[Product]:
    products: list[Product] = []
    i = 0
    while i < len(raw_products):
        if is_vegetable_product(raw_products[i]):
            products.append(
                build_vegetable_product(raw_products[i], raw_products[i + 1])
            )
            i += 1
        else:
            products.append(build_non_vegetable_product(raw_products[i]))
        i += 1
    return products


def is_vegetable_product(raw_product: str) -> bool:
    """A vegetable product does not contain the price at the end of the line, only quantity and name"""
    return re.search(r"\d+,\d+$", raw_product) is None


def build_non_vegetable_product(raw_product: str) -> Product:
    quantity_match = re.search(r"^\d+", raw_product)
    quantity = int(quantity_match.group(0))

    if quantity > 1:
        # In this case, price per unit is also included right before the total price, which is at the end of the line
        price_match = re.search(r" \d+,\d+ \d+,\d+$", raw_product)
        _, __, price_str = price_match[0].split(" ")
    else:
        price_match = re.search(r" \d+,\d+$", raw_product)
        price_str = price_match[0]
    price = float(price_str.replace(",", "."))

    name = raw_product[len(str(quantity)) : price_match.start()]

    return Product(name, quantity, price)


def build_vegetable_product(
    raw_product_first_line: str, raw_product_second_line: str
) -> Product:
    quantity_match = re.search(r"^\d+", raw_product_first_line)
    quantity = int(quantity_match.group(0))
    name = raw_product_first_line[len(str(quantity)) :]

    price_match = re.search(r"\d+,\d+$", raw_product_second_line)
    price = float(price_match.group(0).replace(",", "."))

    return Product(name, quantity, price)
