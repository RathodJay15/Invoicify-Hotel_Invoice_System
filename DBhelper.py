import mysql.connector as mysql

db = mysql.connect(host = "localhost" ,user = "user_name" , password = "password",database = "invoicify")

def insert_customer(name,mobono,addharno,city,address,email):
    cursor = db.cursor()

    insert_query = "INSERT INTO customer (name, aadharno, email, phone, address, city) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, addharno, email, mobono, address, city)
    
    cursor.execute(insert_query, values)
    db.commit()
    customerID = cursor.lastrowid

    return customerID


def insert_invoice(customer_id,total_amount,discount, gst_rate):
    cursor = db.cursor()

    insert_query = "INSERT INTO invoice (CID, total_amount, discount, GST) VALUES (%s, %s, %s, %s)"
    values = (customer_id, total_amount, discount, gst_rate)

    cursor.execute(insert_query, values)
    db.commit()
    invoice_id = cursor.lastrowid

    return invoice_id


def insert_invoice_details(invoice_id,room_bookings):
    cursor = db.cursor()

    insert_query = "INSERT INTO invoice_details (inno, roomno, checkin_date, checkout_date,no_of_nights, price) VALUES (%s, %s, %s, %s, %s, %s)"

    for booking in room_bookings:
        values = (invoice_id, *booking[:5])
        cursor.execute(insert_query, values)

    db.commit()

def get_available_rooms(check_in_date,check_out_date,room_type):
    cursor = db.cursor()
    query = """
        SELECT roomno  FROM room
        WHERE type = %s
          AND roomno NOT IN (
              SELECT roomno FROM invoice_details
              WHERE (%s < checkout_date AND %s > checkin_date)
          )
    """
    cursor.execute(query, (room_type, check_out_date, check_in_date))
    results = cursor.fetchall()

    return results

def get_room_price(room_type , room_no):
    cursor = db.cursor()
    query = """
        SELECT price
        FROM room
        WHERE type = %s AND roomno = %s
    """
    cursor.execute(query, (room_type, room_no))
    result = cursor.fetchone()
    return result
