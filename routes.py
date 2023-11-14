from bottle import Bottle, route, run, jinja2_template as template, static_file, request,redirect
from bottle import response
from models import session, Books
from sqlalchemy import text
from utils.util import Utils
from datetime import datetime
app = Bottle()

@app.get('/static/<filePath:path>')
def index(filePath):
    return static_file(filePath, root='./static')

@app.route('/', method='GET')
def index():
    redirect('/list')

@app.route('/add', method=['GET', 'POST'])
def add():
    view = ""
    registId = ""
    form = {}
    kind = "Registration"
    if request.method == 'GET':
        # If id is specified
        if request.query.get('id') is not None:
            book = session.query(Books).filter(Books.id_==request.query.get('id')).first()
            form['name'] = book.name
            form['volume'] = book.volume
            form['author'] = book.author
            form['publisher'] = book.publisher
            form['memo'] = book.memo
            registId = book.id_

            kind = "edit"

        # Display processing
        return template('add.html'
                , form = form
                , kind=kind
                , registId=registId)
    # POST If
    elif request.method == 'POST':
        # POST Get value
        form['name'] = request.forms.decode().get('name')
        form['volume'] = request.forms.decode().get('volume')
        form['author'] = request.forms.decode().get('author')
        form['publisher'] = request.forms.decode().get('publisher')
        form['memo'] = request.forms.decode().get('memo')
        registId = ""
        # id is specified
        if request.forms.decode().get('id') is not None:
            registId = request.forms.decode().get('id')

        # Validation processing
        errorMsg = Utils.validate(data=form)
        # Display processing
        print(errorMsg)
        if request.forms.get('next') == 'back':
            return template('add.html'
                    , form=form
                    , kind=kind
                    , registId=registId)

        if errorMsg == []:
            # headers = ['著書名', '巻数', '著作者', '出版社', 'メモ']
            headers = ['Book title', 'Volume number', 'Author', 'Publisher', 'Memo']
            return template('confirm.html'
                    , form=form
                    , headers=headers
                    , registId=registId
                    , confirm_title="Confirm Add Record"
                    , confirm_button= "ِAdd")
        else:
            return template('add.html'
                    , error=errorMsg
                    , kind=kind
                    , form=form
                    , registId=registId)

@app.route('/regist', method='POST')
def regist():

    # Receive data
    name = request.forms.decode().get('name');
    volume = request.forms.decode().get('volume');
    author = request.forms.decode().get('author');
    publisher = request.forms.decode().get('publisher');
    memo = request.forms.decode().get('memo');
    registId = request.forms.decode().get('id')

    if request.forms.get('next') == 'back':
        response.status = 307
        response.set_header("Location", '/add')
        return response
    else:
        if registId is not None:
            # Update processing
            books = session.query(Books).filter(Books.id_==registId).first()
            books.name = name
            books.volume = volume
            books.author = author
            books.publisher = publisher
            books.memo = memo
            session.commit()
            session.close()
        else:
            # Data storage process
            books = Books(
                    name = name,
                    volume = volume,
                    author = author,
                    publisher = publisher,
                    memo = memo,
                    create_date = datetime.now().date(), # to be modified by adding
                    delFlag=0)
            session.add(books) 
            session.commit()
            session.close()
        redirect('/list') # Transition to list screen

# Display list of passwords
@app.route('/list')
def passList():
    # Get book list from DB
    bookList = session.query(Books.name, Books.volume, Books.author, Books.publisher, Books.memo, Books.id_)\
            .filter(Books.delFlag == 0).all()
    # headers = ['書名', '巻数', '著者', '出版社', 'メモ','操作']
    headers = ['Book title', 'Volume number', 'Author', 'Publisher', 'Memo', 'Operation']
    return template('list.html', bookList=bookList, headers=headers)

@app.route('/delete/<dataId>', method=['GET', 'POST'])
def delete(dataId):
    ic(dataId)
    # Perform logical delete
    book = session.query(Books).filter(Books.id_==dataId).first()
    headers = ['Book title', 'Volume number', 'Author', 'Publisher', 'Memo']

    form = {}
    form['name'] = book.name
    form['volume'] = book.volume
    form['author'] = book.author
    form['publisher'] = book.publisher
    form['memo'] = book.memo
    
    return template('confirm.html'
                    , form=form
                    , headers=headers
                    , registId=dataId
                    , confirm_title="Confirm Delete Record"
                    , confirm_button= "Delete"
                    , )
    book.delFlg = 1
    session.commit()
    session.close()
    redirect('/list')

@app.route('/deleteX', method='POST')
def registX():

    # Receive data
    name = request.forms.decode().get('name');
    volume = request.forms.decode().get('volume');
    author = request.forms.decode().get('author');
    publisher = request.forms.decode().get('publisher');
    memo = request.forms.decode().get('memo');
    registId = request.forms.decode().get('id')

    if request.forms.get('next') == 'back':
        response.status = 307
        response.set_header("Location", '/add')
        return response
    else:
        if registId is not None:
            # Update processing
            books = session.query(Books).filter(Books.id_==registId).first()
            books.name = name
            books.volume = volume
            books.author = author
            books.publisher = publisher
            books.memo = memo
            session.commit()
            session.close()
        else:
            # Data storage process
            books = Books(
                    name = name,
                    volume = volume,
                    author = author,
                    publisher = publisher,
                    memo = memo,
                    create_date = datetime.now().date(), # to be modified by adding
                    delFlag=0)
            session.add(books) 
            session.commit()
            session.close()
        redirect('/list') # Transition to list screen