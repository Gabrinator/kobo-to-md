import sqlite3
from tabulate import tabulate # For printing pretty tables
from unidecode import unidecode # For replacing curly apostrophes and other unwanted characters
import os

# Get the list of Books for which there are highlights
def get_books(con):
    """Retrieves a list of books with their corresponding number of highlights from the database.

    Args:
        con (sqlite3.Connection): An SQLite Database Connection.

    Returns:
        A list of tuples, where each tuple represents a book and contains:
            - volumeId: The unique identifier of the book (str).
            - BookTitle: The title of the book (str).
            - count(b.BookmarkID): The number of highlights for the book (int).
    """
    
    cur = con.cursor()
    res = cur.execute('SELECT b.volumeId, c.BookTitle, count(b.BookmarkID) FROM Bookmark b LEFT JOIN content c on b.ContentID = c.ContentId GROUP BY b.volumeId;')
    books = res.fetchall()
    print(tabulate(books, headers=['ID','VolumeID', 'BookTitle', 'No. of Highlights'], showindex=True, tablefmt='grid', maxcolwidths=[35,35, None]))
    return books

def get_book_id(books):
    """Prompts the user to select a book by its ID

    Args:
        books (list): A list of books, where each book is represented by a tuple containing:
            - volumeID (str)
            - BookTitle (str)
            - highlightCount (int)

    Returns:
        int: The ID of the selected book
    """

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
    return bookID

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

    try:
        # Create file
        with open(title + '.md', 'x') as f:

            f.write('# ' + title + '\n') # Write the Title of the book
            
            # write Chapter Names
            currentChapter = highlights[0][0]
            f.write('## ' + currentChapter +'\n')
            for row in highlights:
                if row[0] != currentChapter:
                    currentChapter=row[0]
                    f.write('## ' + currentChapter + '\n')

                f.write("> " + unidecode(row[1]) + "\n\n") # write the quote
    except FileNotFoundError as e:
        print(f"Error creating file: {e}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Error writing to file: {e}")


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