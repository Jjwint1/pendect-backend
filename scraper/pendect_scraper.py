from bs4 import BeautifulSoup
import requests as req
import mysql.connector

config = {
    'user': 'root',
    'password': 'demo',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'pendect'
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor(prepared=True)

cursor.execute("""DELETE FROM stories""")

resp = req.get('https://pendect.com/')

soup = BeautifulSoup(resp.text, 'lxml')

links = [title['href'] for title in soup.find_all('a', class_='card-title', href=True)]

for link in links:
    resp = req.get(link)
    soup = BeautifulSoup(resp.text, 'lxml')
    title = soup.find('h1', class_='card-title').text
    img_url = ''
    try:
        img_url = soup.find('img', class_='card-image')['src']
    except:
        img_url = None
    content_card = soup.find('main', class_='card-body')
    content = ''
    ps = content_card.find_all('p')
    for p in ps:
        content += p.text+'\n'

    insert_stmt = """INSERT INTO stories (title, img_url, content) VALUES (%s, %s, %s)"""
    to_insert = (title, img_url, content)
    cursor.execute(insert_stmt, to_insert)


connection.commit()
connection.close()

    