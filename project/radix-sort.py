import urllib
import requests

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    txt = urllib.request.urlopen(book_url).read().decode()
    ascii = txt.encode('ascii','replace')
    return ascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    book_words = book_to_words(book_url)
    max_digits = 0
    for word in book_words:
      length = len(book_words)
      if length > max_digits:
        max_digits = length
    num_iter = len(book_words[max_digits])
    return sorting_book(book_words,num_iter)

def sorting_book(lst, num_iter):
  for n in range(num_iter-1,-1,-1):
    x = [0]*128
    for k in lst:
      try:  
        x[k[n]]+=1
      except:
        x[0]+=1 
    for i in range(1,len(x)):
      x[i] += x[i-1]
    end = [None] * len(lst)
    for i in lst[::-1]:
      try:
        c = i[n]
      except:
        c = 0
      idx = x[c]-1
      end[idx] = i
      x[c]-=1
    lst = end
  return lst

sorting_book()
