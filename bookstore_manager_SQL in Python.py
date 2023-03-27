import sqlite3
db = sqlite3.connect('data/ebookstore_db')
"""1
cursor = db.cursor()

cursor.execute('''
   CREATE TABLE books(id INTEGER PRIMARY KEY, title TEXT,
                   	author TEXT, qty INTEGER)
''')

db.commit()

cursor = db.cursor()

initial_books = [(3001,'A Tale of Two Cities','Charles Dickens',30),
(3002,"Harry Potter and the Philosopher's Stone",'J.K. Rowling',40),
(3003,'The Lion, the Witch and the Wardrobe','C.S.Lewis',25),
(3004,'The Lord of the Rings','J.R.R. Tolkien',37),
(3005,'Alice in Wonderland','Lewis Carroll',12)
]

cursor.executemany(''' INSERT INTO books(id,title,author,qty) VALUES(?,?,?,?)''',initial_books)
db.commit()
db.close()
"""

#The code from line 4 to 24 has been commented out to avoid the interpreter running through the code 
#every time we run our bookstore manager programme
#the initial table has been already created and the first original entries already added to it. 


def enter_book(): 
    '''
    this function will take the input from the user to create a new book record
    and it will add it as a row to the table books
    '''
    cursor = db.cursor()

    new_title = input('Please write the title of the new book:')

    # check if title is already in the database
    cursor.execute(''' SELECT title FROM books WHERE title LIKE ?''',(new_title,))
    control_title = cursor.fetchone()
    
    if control_title:
        control_title_str = ''.join(map(str, control_title))
        if control_title_str.lower() == new_title.lower():
            print('''This title is already in the database, 
                    you can use the update function to change the quantity
            ''')
    else:
        new_author = input('Please write the name of the author:')
        try:
            new_qty = int(input('Please write the available quantity:'))
        except ValueError:
            print('this value is not permitted, quantity must be an integer')  
        else:    
            # fetch the max ID, cast it from tuple to int and increment by 1
            cursor.execute(''' SELECT MAX(id) FROM books''')
            new_id = cursor.fetchone()
            new_id = int(''.join(map(str, new_id)))
            new_id += 1
   
            cursor.execute(''' INSERT INTO books(id,title,author,qty) VALUES(?,?,?,?)''',(new_id,new_title,new_author,new_qty))
            db.commit()
            print('Your new book has been succesfully added to the list')


def update_book():
    '''
    this function will only update a book based on its ID 
    '''
    print(
    '''
    You can only update a book if you know its ID
    If you don't know it please use the search function to find it
    ''')

    know_book_id = input('Do you know the book ID?(Y/N):').lower()

    if know_book_id == 'y':
        cursor = db.cursor()
        try:
            book_id = int(input('Please type the book ID:'))
        except ValueError:
            print('this value is not permitted, id must be an integer')
        else:
            cursor.execute(''' SELECT id FROM books WHERE id = ?''',(book_id,))
            verified_id = cursor.fetchone()
        
            if verified_id:
                cursor = db.cursor()
                cursor.execute(''' SELECT * FROM books WHERE id =?''',(book_id,))
                book_info = cursor.fetchone()
                print(f'Here are all the information regarding the selected book: {book_info}')

                feat_to_update = input('''
                Select which part of the record you'd like to update:
                t - title
                a - author
                q - quantity
                ''').lower()
                if feat_to_update == 't':
                    cursor = db.cursor()
                    update_title = input('Please type the new title:')
                    cursor.execute(''' UPDATE books SET title = ? WHERE id =?''',(update_title,book_id))
                    db.commit()
                elif feat_to_update == 'a':
                    cursor = db.cursor()
                    update_author = input('Please type the new author:')
                    cursor.execute(''' UPDATE books SET author = ? WHERE id =?''',(update_author,book_id))
                    db.commit()
                elif feat_to_update == 'q':
                    cursor = db.cursor()
                    update_qty = int(input('Please type the new quantity:'))
                    cursor.execute(''' UPDATE books SET qty = ? WHERE id =?''',(update_qty,book_id))
                    db.commit()
                else:
                    print('Sorry, this choice is invalid')
            else:
                print("Sorry, this ID couldn't be found in the database")
    elif know_book_id == 'n':
        print("Choose search in the main menu to find the neccesarry ID")
    else:
        print("This answer is invalid. You can find the ID with the search option")


def delete_book():
    '''
    deleting a book from the database is permanent
    for safety, this function can only delete a book based on its ID
    '''
    print(
    '''
    You can only delete a book if you know its ID
    If you don't know it please use the search function to find it
    ''')

    know_book_id = input('Do you know the book ID?(Y/N):').lower()

    if know_book_id == 'y':
        cursor = db.cursor()
        try:
            book_id = int(input('Please type the book ID:'))
        except ValueError:
            print('this value is not permitted, id must be an integer')
        else:
            cursor.execute(''' SELECT id FROM books WHERE id =?''',(book_id,))
            verified_id = cursor.fetchone()
        
            if verified_id:
                cursor = db.cursor()
                cursor.execute(''' SELECT title FROM books where id =?''',(book_id,))
                book_title = cursor.fetchone()
                cursor.execute(''' DELETE FROM books where id =?''',(book_id,))
                db.commit()
                print(f'The book {book_title} with ID:{book_id} has been successfully deleted from the table')
            else:
                print("Sorry, this ID couldn't be found in the database")
    
    elif know_book_id == 'n':
        print("Choose search in the main menu to find the neccesarry ID")
    else:
        print("This answer is invalid. You can find the ID with the search option")

def search_book():
    '''
    this function allows the user to search a books in the database
    based on title, author or id
    '''
    print('''
    This function allows you to search a book by the title , the author or the ID
    ''')
    search_choice = input('''
    What will you base your search on?
    t - title 
    a - author
    i - id
    ''')

    if search_choice == 't':
        cursor = db.cursor()
        search_title = input('Please type the title:').lower()
        cursor.execute(''' SELECT * FROM books WHERE title LIKE ?''',(search_title,))
        print('\nHere are the books found:')
        for row in cursor:
            print(row)
    elif search_choice == 'a':
        cursor = db.cursor()
        search_author = input('Please type the author:').lower()
        cursor.execute(''' SELECT * FROM books WHERE author LIKE ?''',(search_author,))
        print('\nHere are the books found:')
        for row in cursor:
            print(row)
    elif search_choice == 'i':
        cursor = db.cursor()
        try:
            search_id = int(input('Please type the id:'))
        except ValueError:
            print('this value is not permitted, id must be an integer')
        else:    
            cursor.execute(''' SELECT * FROM books WHERE id = ?''',(search_id,))
            print('\nHere are the books found:')
            for row in cursor:
                print(row)
    else:
        print('Sorry, that choice is not valid')


#########################
# Main Program
######################### 

while True:
    # Get input from user
    menu = input('''
    BOOKSTORE MANAGER 1.0
    Please type the number to select the option:
    1 - Enter book
    2 - Update book
    3 - Delete book
    4 - Search book
    0 - Exit
    : ''')
# enter a new book
    if menu == '1':     
        enter_book()
# update a book
    elif menu == '2': 
        update_book()
# delete a book       
    elif menu == '3':       
        delete_book()
# search a book
    elif menu == '4':    
       search_book()
        
# Exit program
    elif menu == '0': 
        print('Goodbye!!!')
        db.close()
        exit()
# Default case
    else: 
        print("You have made a wrong choice, Please Try again")
   