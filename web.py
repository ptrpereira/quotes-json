from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

app = Flask(__name__)

@app.route('/api/v1/quotes', methods=['GET'])
def quotes():
    url = "https://quotabulary.com/short-meaningful-quotes"

    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for contBox in soup.find_all("div", class_="bz-card bz-basic-card layout1 theme5 br-all title-fs-md mt-3 title-clr-1"):        
        quoteFull = contBox.find("div", class_="bz-text").text.strip()
        rm = quoteFull.find(" -")
        quoteObj = quoteFull[0:rm]
        authorObj = contBox.find("div", class_="bz-text").find("strong").text.strip()
        
        data.append({'quote': quoteObj,
                    'author': authorObj})

    return jsonify({'quotes': data})
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
