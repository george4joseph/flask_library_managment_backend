

from urllib import response
from flask import Flask, render_template, flash, request
import sqlite3
import json, urllib, requests
from importlib_metadata import re
from datetime import date, datetime,timedelta
# creating file path
dbfile = '/home/mary/Desktop/ma/Libm.db'

app = Flask(__name__)

# Add member
@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/vnd.api+json'):
            json_ = request.get_json()
            name = json_["name"]
            email = json_["email"]
            # Creating a SQL connection to our SQLite database
            con = sqlite3.connect(dbfile)
            # creating cursor
            cur = con.cursor()
            # Executing SQL Query
            cur.execute("INSERT INTO members (name, email,books_issued,total_debt) VALUES (?,?,0,0)", (name, email))
            # commiting
            con.commit()
            # closing
            cur.close()
            return ("Sucess")
        
    if request.method == 'GET':
        # Create a SQL connection to our SQLite database
        con = sqlite3.connect(dbfile)
        # creating cursor
        cur = con.cursor()
        # Execute SQL Query
        result = cur.execute("SELECT * FROM members")
        members = cur.fetchall()
        cur.close()
        return (members)

#  Update,Get and Delete member using ID
@app.route('/member/<string:id>', methods=['GET', 'PATCH','DELETE'])
def update_member(id):
    if request.method == 'PATCH':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/vnd.api+json'):
            json_ = request.get_json()
            name = json_["name"]
            email = json_["email"]
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            cur.execute("UPDATE members SET name=?, email=? where id=?", (name, email,id))
            con.commit()
            cur.close()
            return ("UPDATED") 

    if request.method == 'GET':
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        result = cur.execute("SELECT * FROM members WHERE id=?",(id,))
        members = cur.fetchall()
        cur.close()
        return (members)

    if request.method == 'DELETE':
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            cur.execute("DELETE from members where id= ?", (id,))
            con.commit()
            cur.close()
            return ("DELETEDDD")    

# Books
@app.route('/books', methods=['GET','POST'])
def books():
    if request.method == 'GET':
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        result = cur.execute("SELECT * FROM books")
        books = cur.fetchall()
        cur.close()
        return (books)
    
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/vnd.api+json'):
            json_ = request.get_json()

            bookID = json_["bookID"]
            title = json_["title"]
            authors = json_['authors']
            average_rating = json_['average_rating']
            isbn= json_['isbn']
            isbn13 = json_['isbn13']
            language_code = json_['language_code']
            num_pages = json_["  num_pages"]
            ratings_count  = json_['ratings_count']
            text_reviews_count = json_['text_reviews_count']
            publication_date = json_['publication_date']
            publisher = json_['publisher']
            total_quantity = json_['total_quantity']
            available_quantity = json_['available_quantity']

            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            cur.execute("INSERT INTO books (bookID,title,authors,average_rating,isbn,isbn13 ,language_code ,num_pages,ratings_count ,text_reviews_count ,publication_date,publisher,total_quantity,available_quantity) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                bookID,title,authors,average_rating,isbn,isbn13 ,language_code ,num_pages,ratings_count ,text_reviews_count ,publication_date,publisher,total_quantity,available_quantity
            ))
            con.commit()
            cur.close()
            return ("Sucess")

@app.route('/book/<string:id>', methods=['GET', 'PATCH','DELETE'])
def book_update(id):
    if request.method == 'PATCH':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/vnd.api+json'):
            json_ = request.get_json()

            title = json_["title"]
            authors = json_['authors']
            average_rating = json_['average_rating']
            isbn= json_['isbn']
            isbn13 = json_['isbn13']
            language_code = json_['language_code']
            num_pages = json_["  num_pages"]
            ratings_count  = json_['ratings_count']
            text_reviews_count = json_['text_reviews_count']
            publication_date = json_['publication_date']
            publisher = json_['publisher']
            total_quantity = json_['total_quantity']
            available_quantity = json_['available_quantity']

            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            cur.execute("UPDATE books SET title=?,authors=?,average_rating=?,isbn=?,isbn13 =?,language_code =?,num_pages=?,ratings_count =?,text_reviews_count =?,publication_date=?,publisher=?,total_quantity =?,available_quantity=? where bookID=?",
             (title,authors,average_rating,isbn,isbn13 ,language_code ,num_pages,ratings_count ,text_reviews_count ,publication_date,publisher,total_quantity,available_quantity, id))
            con.commit()
            cur.close()
            return ("UPDATED") 

    if request.method == 'GET':
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        result = cur.execute("SELECT * FROM books WHERE bookID=?",(id,))
        book = cur.fetchall()
        cur.close()
        return (book)

    if request.method == 'DELETE':
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        cur.execute("DELETE from books where bookID= ?", (id,))
        con.commit()
        cur.close()
        return ("DELETEDDD")    

# import frappe 
@app.route('/import',methods=['POST','GET'])
def import_book():
    
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/vnd.api+json' and request.method == 'POST'):
        json_ = request.get_json()
        url = 'https://frappe.io/api/method/frappe-library?'
        parameters = {'page': 1}
        if 'title' in json_.keys():
            parameters['title'] = json_['title']
        if 'authors' in json_.keys():
            parameters['authors'] = json_['authors']
        if 'isbn' in json_.keys():
            parameters['isbn'] = json_['isbn']
        if 'publisher' in json_.keys():
            parameters['publisher'] = json_['publisher']
        

        no_of_books = json_['no_of_books']
        quantity = json_['quantity']
        imported_count = 0
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        # Counting as many books are imported
        while (no_of_books != imported_count):
            req = requests.get(url + urllib.parse.urlencode(parameters))
            response = req.json()
            if not response['message']:
                return (f"UPDAEDF new books: {imported_count}")
                
            
            # Checking each book in resposne
            for each_book in response['message']:
                result = cur.execute("SELECT * FROM books WHERE bookID=?",(each_book['bookID'],))
                book_exist = cur.fetchone()
        
                if imported_count == no_of_books:
                    return (f"UPDAEDF new books: {imported_count}")
                if not book_exist:
                    cur.execute("INSERT INTO books (bookID,title,authors,average_rating,isbn,isbn13 ,language_code ,num_pages,ratings_count ,text_reviews_count ,publication_date,publisher,total_quantity,available_quantity) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                        each_book['bookID'],
                        each_book['title'],
                        each_book['authors'],
                        each_book['average_rating'],
                        each_book['isbn'],
                        each_book['isbn13'],
                        each_book['language_code'],
                        each_book['  num_pages'],
                        each_book['ratings_count'],
                        each_book['text_reviews_count'],
                        each_book['publication_date'],
                        each_book['publisher'],quantity,quantity))
                else:
                    cur.execute("UPDATE books SET total_quantity=total_quantity + ?, available_quantity=available_quantity + ? where bookID=?",(quantity,quantity,each_book['bookID']))

                imported_count += 1   
                con.commit()
            parameters['page'] = parameters['page'] + 1

            
        cur.close()
        return (f"UPDAEDF new books: {imported_count}")



# Transactions
@app.route('/transactions', methods=['GET'])
def all_transactions():
    if request.method == 'GET':
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        result = cur.execute("SELECT * FROM transactions")
        transactions = cur.fetchall()
        cur.close()
        return (transactions)

# issue book
@app.route('/issue', methods=['POST'])
def issue():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/vnd.api+json' and request.method == 'POST'):
        json_ = request.get_json()
        member_id = json_['memberID']
        book_id = json_['bookID']
        rent = json_['rent_per_day']
        # connecting db
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        # check dept >500 and stock of book exist 
        cur.execute("SELECT books_issued,total_debt from members where id=?",(member_id,))
        issued_count_debt = cur.fetchall()
        # only 3 books can be issued to a member
        if issued_count_debt[0][0] == 3:
            return("U have issued 3 books - return one and take book")
        if issued_count_debt[0][1] >= 500:
            return("Your debt is high- plz pay")

        # get stocks of books
        cur.execute("SELECT available_quantity from books where bookID=?",(book_id,))
        avail_quantity = cur.fetchall()
        if avail_quantity[0][0] == 0:
            return("Book stock finished")
        # due date is 10 days from existing date
        today = date.today()
        due_date = today + timedelta(days=10)
        total_charge= 10 * rent
        #  inserting into transactions
        result = cur.execute("INSERT INTO transactions (memberID, bookID, rent_per_day, issued_on, due_date, total_charge) VALUES (?,?,?,?,?,?)",(member_id,book_id,rent,today,due_date,total_charge))

        cur.execute("UPDATE books set available_quantity = available_quantity-1 where bookID=?",(book_id,))
        # update in member table
        cur.execute("UPDATE members set books_issued = books_issued + 1, total_debt = total_debt +?  where id=?",(total_charge,member_id))
        con.commit()
        cur.close()
        return ("issued")


# renew for 5 days
@app.route('/renew', methods=['POST'])
def renew():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/vnd.api+json' and request.method == 'POST'):
        json_ = request.get_json()
        member_id = json_['memberID']
        book_id = json_['bookID']
        # renew days are from date of due date
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        # Getting existing due date
        cur.execute("SELECT due_date,rent_per_day FROM transactions where bookID=? and memberID=?",(book_id,member_id))
        cur_due_date_rent = cur.fetchall()
        cur_due_date_obj = datetime.strptime(cur_due_date_rent[0][0],"%Y-%m-%d").date()
        today = date.today()
        if today > cur_due_date_obj:
            return("Cannot renue- plz return")
        # renewd date
        new_due_date_obj = cur_due_date_obj + timedelta(days=5)
        renewed_charge = 5 * cur_due_date_rent[0][1]
        # update the transactions
        cur.execute("UPDATE transactions SET due_date=?,total_charge=total_charge +? WHERE bookID=? and memberID=?",(new_due_date_obj,renewed_charge,book_id,member_id))
        cur.execute("UPDATE members set total_debt = total_debt +?  where id=?",(renewed_charge,member_id))
        con.commit()
        cur.close()
        return ("renewed")

# return
app.route('/return',methods=['POST'])
def return_():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/vnd.api+json' and request.method == 'POST'):
        json_ = request.get_json()
        member_id = json_['memberID']
        book_id = json_['bookID']
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        # getting data from db
        today = date.today()
        cur.execute("SELECT issued_on,rent_per_day FROM transactions where bookID=? and memberID=?",(book_id,member_id))
        issue_date_rent = cur.fetchall()
        date_time_obj = datetime.strptime(issue_date_rent[0])
        rent_per_day = issue_date_rent[1]
        book_in_hand_days = (today - date_time_obj).days
        if book_in_hand_days > 10 :
            # pay punishment charge
            # charge is 1.5 times 
            additional_charge = (book_in_hand_days - 10) * 2 * rent_per_day

            cur.execute("UPDATE transactions SET returned =?,total_charge= total_charge + ? where bookID=? and memberID=?",(str(today),additional_charge,book_id,member_id))




    










