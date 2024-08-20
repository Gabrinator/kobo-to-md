# kobo-to-md
 Takes Kobo Highlights and exports them to a markdown file.

 ## Usage
 1. Navigate to the folder containing KoboReader.sqlite
 2. Run the program. It will list the available books with highlights
 3. Type in the ID of the book for which you would like to export highlights
 4. This will create a markdown file named after the book title in the same directory.

 ## WIP
 * Add error handling, especially for user input but also file and db
 * Commandline arguments
    * config (+ config file for default db and export locations)
    * list - to list available books
    * specify output file name
    * specify input file name
