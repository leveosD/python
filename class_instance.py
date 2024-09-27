class Book:
    title = None
    pages = None
    price = None

    def __init__(self, title, pages, price):
        self.title = title
        self.pages = pages
        self.price = round(price, 2)

    def more_pages(self):
        self.pages += 10

    def discount(self):
        if self.pages > 100:
            self.price /= 2

    def get_info(self):
        print("Название книги:", self.title, '.', self.pages, "страниц.", int(self.price), "рублей", int(self.price * 100 % 100), "копеек.")

book1 = Book("Мобби Дик", 704, 278.44)
title = ''
while title == '' or title.split() == []:
    title = input("Введите название книги:")
res = ''
for s in title.split():
    res += s + ' '
res = res[:-1]
pages = input("Введите количество страниц:")
while not pages.isdigit() or int(pages) <= 0 or int(pages) >= 10**5:
    pages = input("Введите количество страниц:")
pages = int(pages)
price = ''
while type(price) != float:
    price = input("Введите цену(руб.коп):")
    try:
        if 0 <= float(price) <= 10**12 and ((price.find('.') != -1 and 0 < len(price.split('.')[1]) <= 2) or price.find('.') == -1):
            price = float(price)
    except:
        continue

book2 = Book(res, pages, price)
title = "Колобок"
pages = 10
price = 149.333
book3 = Book(title, pages, price)

book1.get_info()
book2.get_info()
book3.get_info()

book1.more_pages()

book2.more_pages()
book2.discount()

book3.more_pages()
book3.discount()

book1.get_info()
book2.get_info()
book3.get_info()
