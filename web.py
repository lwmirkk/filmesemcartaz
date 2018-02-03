from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os   

app = Flask(__name__)

#Criar GetByID: http://blog.luisrei.com/articles/flaskrest.html

@app.route('/api/v1/filmes', methods=['GET'])
def filmes():
    URL = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/"
    
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for dataBox in soup.find_all("div", class_="data_box"):
        titleObj = dataBox.find("a", class_="no_underline")
        imgObj = dataBox.find(class_="img_side_content").find_all(class_="acLnk")[0]
        sinopseObj = dataBox.find("div", class_="content").find_all("p")[0]
        dateObj = dataBox.find("div", class_="content").find("div", class_="oflow_a")
        movieLinkObj = dataBox.find(class_="img_side_content").find_all("a")[0]
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="synopsis-txt")        

        data.append({'titulo': titleObj.text.strip(),
                    'poster' : imgObj.img['src'].strip(), #.decode_contents(formatter="html")
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj.text[0:11].strip(),
                    'link' : detailsLink,
                    'sinopseFull': fullSinopse.text})
                
    return jsonify({'filmes': data})  

@app.route('/api/v1/filmes/<page_id>', methods=['GET'])
def NotasEspectadores(page_id):
    URL = "http://www.adorocinema.com/filmes/todos-filmes/notas-espectadores/?page={}".format(page_id)
    
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    data = []
    for dataBox in soup.find_all("div", class_="data_box"):
        titleObj = dataBox.find("a", class_="no_underline")
        imgObj = dataBox.find(class_="img_side_content").find_all(class_="acLnk")[0]
        sinopseObj = dataBox.find("div", class_="content").find_all("p")[0]
        dateObj = dataBox.find("div", class_="content").find("div", class_="oflow_a")
        movieLinkObj = dataBox.find(class_="img_side_content").find_all("a")[0]
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="synopsis-txt")        

        data.append({'titulo': titleObj.text.strip(),
                    'poster' : imgObj.img['src'].strip(), #.decode_contents(formatter="html")
                    'sinopse' : sinopseObj.text.strip(),
                    'data' :  dateObj.text[0:11].strip(),
                    'link' : detailsLink,
                    'sinopseFull': fullSinopse.text})
                
    return jsonify({'filmes': data})    

@app.route('/api/v1/filmes/emcartaz/<page_id>', methods=['GET'])
def EmCartaz():
    URL = "http://www.adorocinema.com/filmes/numero-cinemas/".format(page_id)
    
    html_doc = urlopen(URL).read()
    soup = BeautifulSoup(html_doc, "html.parser")

    data = []
    for dataBox in soup.find_all("div", class_="card card-entity card-entity-list cf"):
        nomeObj = dataBox.find("h2", class_="meta-title")
        imgObj = dataBox.find(class_="thumbnail ")
        sinopseObj = dataBox.find("div", class_="synopsis")
        dataObj = dataBox.find(class_="meta-body").find(class_="meta-body-item meta-body-info")
        movieLinkObj = dataBox.find(class_="meta-title-link")
        detailsLink = 'http://www.adorocinema.com' + movieLinkObj.attrs['href']

        #LOAD FULL SINOPSE 
        htmldocMovieDetail = urlopen(detailsLink).read()
        soupMovieDetail = BeautifulSoup(htmldocMovieDetail, "html.parser")
        fullSinopse = soupMovieDetail.find(class_="synopsis-txt")        

        data.append({   'nome': nomeObj.text.strip(),
                        'poster' : imgObj.img['data-src'].strip(),
                        'sinopse' : sinopseObj.text.strip(),
                        'data' :  dataObj.text[1:23].strip().replace('/',' '),
                        'link' : detailsLink,
                        'sinopseFull': fullSinopse.text})
                
    return jsonify({'filmes': data})

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    # Tem que ser 0.0.0.0 para rodar no Heroku
    app.run(host='0.0.0.0', port=port)
