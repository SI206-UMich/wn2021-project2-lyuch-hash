import bs4
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
  
    lst=[]
    lst_1=[]
    lst_2=[]
    
    file=open(filename)
    var=file.read()
    file.close()
    soup=BeautifulSoup(var,'html.parser')
    tag_1=soup.find_all('a',class_='bookTitle')
    for teg in tag_1:
        tegg=teg.text.strip('\n')
        lst_1.append(tegg)
    
    tag_2=soup.find_all('span',itemprop='author')
    for tegg in tag_2:
        tegg_1=tegg.find_all('a',class_="authorName")[0].text.strip('\n')
        lst_2.append(tegg_1)
       
    for i in range(len(lst_1)):
        lst.append((lst_1[i],lst_2[i]))
    return lst
    


def get_search_links():
  
    lst=list()
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tags = soup.find_all('a',class_="bookTitle")
    
    for tag in tags[:10]:
        gg=tag['href']
        
        if gg.startswith('/book/show'):
            lst.append('https://www.goodreads.com'+gg)
    
    
           
    return lst
    
    
    
    


def get_book_summary(book_url):
 
    
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tup=tuple()
    tag_1=soup.find('h1').text.strip('\n').strip()
    tag_2=soup.find('a',class_='authorName').text.strip('\n').strip()
    tag=soup.find('div',class_='row')
    
    tag_3=tag.find('span',itemprop="numberOfPages").text.strip('\n').split()
    tag_3=int(tag_3[0])
    tup=(tag_1,tag_2,tag_3)
    return tup

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """    
    catelist=[]
    
    with open(filepath,encoding='utf8') as f:
         soup=BeautifulSoup(f,'html.parser')
    lt=soup.find('div',class_="categoryContainer")
    lst=lt.find_all('div',class_="category clearFix")
    for i in lst:
        ii=i.find('a')
        tup=tuple()
        a=ii.find('h4',class_="category__copy").text.strip('\n')
        bb=ii.find('div',class_="category__winnerImageContainer")
        b=bb.find('img')['alt']
        c=ii.get('href',None)
        tup=(a,b,c)
        catelist.append(tup)
    return catelist
    
        
    
    
    
    
    
    



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1 
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='') as csvfile:
            csv_writer=csv.writer(csvfile,delimiter=',')
            
            csv_writer.writerow(['Book Title','Author Name'])
            for i in data:
                
                csv_writer.writerow(i)
    


class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        loc=get_titles_from_search_results("search_results.htm")
        self.assertEqual(len(loc),20)
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(type(loc),list)
        # check that the variable you saved after calling the function is a list
        for x in loc:
            self.assertEqual(type(x),tuple)
        # check that each item in the list is a tuple
        
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(loc[0],("Harry Potter and the Deathly Hallows (Harry Potter, #7)","J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(loc[19],("Harry Potter: The Prequel (Harry Potter, #0.5)","J.K. Rowling"))
   
    def test_get_search_links(self):
        
        self.assertEqual(type(get_search_links()),list)
        self.assertEqual(len(get_search_links()),10)
        

        a=get_search_links()
        for i in a:
        # check that each URL in the TestCases.search_urls is a string
            self.assertEqual(type(i),str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertTrue(i.startswith("https://www.goodreads.com/book/show/"))
        
   # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        
        summaries=[]
        a=get_search_links()
        for i in a:
            summaries.append(get_book_summary(i))
        
        
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries),10)
            # check that each item in the list is a tuple
        for u in summaries:
            self.assertEqual(type(u),tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(u),3)
            # check that the first two elements in the tuple are string
            self.assertTrue((type(u[0])==str)and(type(u[1])==str))
            # check that the third element in the tuple, i.e. pages is an int
            self.assertTrue(type(u[2])==int)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2],337)
    
    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        filepath=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'best_books_2020.htm')
        var=summarize_best_books(filepath)
        # check that we have the right number of best books (20)
        self.assertEqual(len(var),20)
            # assert each item in the list of best books is a tuple
        for i in var:
            self.assertEqual(type(i),tuple)
            self.assertEqual(len(i),3)
            # check that each tuple has a length of 3
        self.assertEqual(var[0],('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(var[-1],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        a=get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(a,'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as file:

            csv_lines=csv.reader(file)
            
            csv_line=[]
            for i in csv_lines:
                csv_line.append(i)
            
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_line),21)
        # check that the header row is correct
        self.assertEqual(csv_line[0],['Book Title','Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_line[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])                                                             
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_line[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])


if __name__ == '__main__':
   
    unittest.main(verbosity=2)
