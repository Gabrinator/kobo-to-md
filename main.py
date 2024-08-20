import sqlite3
from tabulate import tabulate
from unidecode import unidecode

# Get the list of Books for which there are highlights
def get_books(con):
    cur = con.cursor()
    res = cur.execute('SELECT b.volumeId, c.BookTitle, count(b.BookmarkID) FROM Bookmark b LEFT JOIN content c on b.ContentID = c.ContentId GROUP BY b.volumeId;')
    books = res.fetchall()
    print(tabulate(books, headers=['ID','VolumeID', 'BookTitle', 'No. of Highlights'], showindex=True, tablefmt='grid', maxcolwidths=[35,35, None]))
    return books

def to_markdown(con, books, bookID):

    title = books[bookID][1]
    if title == None:
        title= input("What should the title of the book be?")

    # Create file
    f = open(title + '.md', 'x')
    f.write('# ' + title + '\n') # Write the Title of the book

    # get the highlights
    cur = con.cursor()
    res = cur.execute("""SELECT c.Title as Chapter, Text , b.ChapterProgress
FROM Bookmark b LEFT JOIN content c ON b.ContentId=c.ContentId 
WHERE volumeId='""" + books[bookID][0] + """' ORDER BY Chapter ASC, b.ChapterProgress ASC;""")
    highlights=res.fetchall()
    
    # write the different quotes
    currentChapter = highlights[0][0]
    f.write('## ' + currentChapter +'\n')
    for row in highlights:
        if row[0] != currentChapter:
            currentChapter=row[0]
            f.write('## ' + currentChapter + '\n')

        f.write("> " + unidecode(row[1]) + "\n\n")
    f.close()


con = sqlite3.connect('KoboReader.sqlite') # default filename

print("Welcome to Kobo to Markdown")
print("The following books have highlights:")

books = get_books(con)

# Get the book number for which to extract
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


to_markdown(con, books, bookID)

# Close the DB connnection
con.close()