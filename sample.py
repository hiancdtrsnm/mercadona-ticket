from mercadona.ticket_parser.parser import build_ticket

ticket = build_ticket("example/example.pdf")

print(f"Bought at: {ticket.bought_at}")
print("Products:")
for product in ticket.products:
    print(f"  - {product.name}: {product.price}€ X {product.quantity}")
