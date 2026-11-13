# Diagrama de classes

A fatura agrega o cliente e os livros comprados, e cada livro agrega o seu autor. O GitHub desenha o diagrama abaixo a partir do texto.

```mermaid
classDiagram
    direction LR
    class Invoice {
        -int id
        -Customer customer
        -int nBooks = 0
        -Book[] books
        -int[] quantities
        +Invoice(id: int, customer: Customer)
        +getId() int
        +getCustomer() Customer
        +addBook(book: Book, quantity: int) bool
        +removeBook(book: Book) bool
        +getTotal() double
        +getTotalAfterDiscount() double
        +equals(another: Invoice) bool
        +toString() String
    }
    class Customer {
        -int id
        -String name
        -int discount
        +Customer(id: int, name: String, discount: int)
        +getId() int
        +getName() String
        +getDiscount() int
        +setDiscount(discount: int) void
        +equals(another: Customer) bool
        +toString() String
    }
    class Book {
        -int id
        -String name
        -Author author
        -double price = 0.0
        +Book(id: int, name: String, author: Author)
        +Book(id: int, name: String, author: Author, price: double)
        +getName() String
        +getAuthor() Author
        +getPrice() double
        +setPrice(price: double) void
        +equals(another: Book) bool
        +toString() String
    }
    class Author {
        -int id
        -String name
        -char gender
        +Author(id: int, name: String, gender: char)
        +getId() int
        +getName() String
        +getGender() char
        +equals(another: Author) bool
        +toString() String
    }
    Invoice o-- "1" Customer
    Invoice o-- "m" Book
    Book o-- "1" Author
```

| Classe | Formato do `toString` | Observação |
|---|---|---|
| `Invoice` | `Invoice[id = ?, Customer[id = ?, name = ?, discount = ?], total = ?]` | O total já sai com o desconto. `addBook` devolve `false` se o livro já estiver na fatura, e `removeBook`, se ele não estiver. |
| `Customer` | `Customer[id = ?, name = ?, discount = ?]` | O desconto é um percentual de 0 a 100. |
| `Book` | `Book[name = ?, Author[name = ?, gender = ?], price = ?]` | O título é guardado com até 63 bytes. |
| `Author` | `Author[name = ?, gender = ?]` | O gênero vale `M` ou `F`. |
