import sqlite3
from tabulate import tabulate # For printing pretty tables
from unidecode import unidecode # For replacing curly apostrophes and other unwanted characters
import os

# Get the list of Books for which there are highlights
def get_books(con):
    cur = con.cursor()
    res = cur.execute('SELECT b.volumeId, c.BookTitle, count(b.BookmarkID) FROM Bookmark b LEFT JOIN content c on b.ContentID = c.ContentId GROUP BY b.volumeId;')
    books = res.fetchall()
    print(tabulate(books, headers=['ID','VolumeID', 'BookTitle', 'No. of Highlights'], showindex=True, tablefmt='grid', maxcolwidths=[35,35, None]))
    return books

def get_book_id(books):
    while True:
        try:
            bookID = int(input("Enter the ID of the book for which you would like to export highlights: "))
        except ValueError:
            print('Not a valid number')
            continue
        if bookID > len(books) -1 or bookID < 0:
            print('The number does not correspond to an existing book. Please enter a valid ID number.')
        else:
            break

def get_highlights(con, books, bookID):
    # get the highlights
    cur = con.cursor()
    res = cur.execute("""SELECT c.Title as Chapter, Text , b.ChapterProgress
        FROM Bookmark b LEFT JOIN content c ON b.ContentId=c.ContentId 
        WHERE volumeId='""" + books[bookID][0] + """' ORDER BY Chapter ASC, b.ChapterProgress ASC;""")
    highlights=res.fetchall()
    return highlights

def to_markdown(highlights, books, bookID):

    title = books[bookID][1]
    if title == None:
        title= input("What should the title of the book be?")

    # Create file
    f = open(title + '.md', 'x')
    f.write('# ' + title + '\n') # Write the Title of the book
    
    # write the different quotes
    currentChapter = highlights[0][0]
    f.write('## ' + currentChapter +'\n')
    for row in highlights:
        if row[0] != currentChapter:
            currentChapter=row[0]
            f.write('## ' + currentChapter + '\n')

        f.write("> " + unidecode(row[1]) + "\n\n")
    f.close()


def main():

    dbfile = 'KoboReader.sqlite'
    # Check if the file exists
    if os.path.isfile(dbfile):

        try:

            con = sqlite3.connect(dbfile) # default filename
            books = get_books(con)

            print("Welcome to Kobo to Markdown")
            print("The following books have highlights:")

            # Get the book number for which to extract
            bookID = get_book_id(books)

            highlights = get_highlights(con, books, bookID)
            to_markdown(highlights, books, bookID)

        except sqlite3.Error as e:
            print(f"Error accessing database: {e}")

        finally:
            # Close the DB connnection
            if con:
                con.close()
    else: 
        print('Database file not found. Please ensure you are in the same folder as KoboReader.sqlite.')


if __name__ == "__main__":
    main()