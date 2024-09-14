import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database=""
)


def get_database_documents():
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT asset_id, filename, uri_source, firstpagetxt, extension, md_created_on, md_numpages, md_author FROM core_assets where item_type = 'document' and firstpagetxt is not null ORDER BY md_charcount asc")
    myresult = mycursor.fetchall()
    return myresult
