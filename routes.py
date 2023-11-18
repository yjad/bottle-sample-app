from datetime import datetime
from bottle import Bottle, route, run, jinja2_template as template, static_file, request,redirect
from bottle import response
from models import session, Books
from sqlalchemy import text
from utils.util import Utils
from icecream import ic


app = Bottle()

def book_2_form(book):
    form = {}
    form['name'] = book.name
    form['volume'] = book.volume
    form['author'] = book.author
    form['publisher'] = book.publisher
    form['memo'] = book.memo
    return form

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
    # kind = "登録"
    kind = "Registration"
    if request.method == 'GET':
        # id指定された場合
        # If id is specified
        if request.query.get('id') is not None:
            book = session.query(Books).filter(Books.id_==request.query.get('id')).first()
            form['name'] = book.name
            form['volume'] = book.volume
            form['author'] = book.author
            form['publisher'] = book.publisher
            form['memo'] = book.memo
            registId = book.id_

            # kind = "編集"
            kind = "edit"

          # Display processing
        return template('add.html'
                , form = form
                , kind=kind
                , registId=registId)
    # POSTされた場合
    elif request.method == 'POST':
        # POST値の取得
        form['name'] = request.forms.decode().get('name')
        form['volume'] = request.forms.decode().get('volume')
        form['author'] = request.forms.decode().get('author')
        form['publisher'] = request.forms.decode().get('publisher')
        form['memo'] = request.forms.decode().get('memo')
        registId = ""
        # idが指定されている場合
        if request.forms.decode().get('id') is not None:
            registId = request.forms.decode().get('id')

        # バリデーション処理
        # id is specified
        errorMsg = Utils.validate(data=form)
        # 表示処理
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
                    , registId=registId)
        else:
            return template('add.html'
                    , error=errorMsg
                    , kind=kind
                    , form=form
                    , registId=registId)

@app.route('/confirm', method='POST')
def confirm():

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
    else:   # confirm of edit
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
            # Confirm of add record
            books = Books(
                    name = name,
                    volume = volume,
                    author = author,
                    publisher = publisher,
                    memo = memo,
                    create_date = datetime.now().date(),
                    del_flag = 0,
                    )
            session.add(books) 
            session.commit()
            session.close()
        redirect('/list') # Transition to list screen

# Display list of Books
@app.route('/list')
def passList():
    # Get book list from DB
    bookList = session.query(Books.name, Books.volume, Books.author, Books.publisher, Books.memo, Books.id_)\
            .filter(Books.del_flag == 0).all()
    # headers = ['書名', '巻数', '著者', '出版社', 'メモ','操作']
    headers = ['Book title', 'Volume number', 'Author', 'Publisher', 'Memo', 'Operation']
    return template('list.html', bookList=bookList, headers=headers)

@app.route('/delete/<dataId>', method=['GET', 'POST'])
def delete(dataId):
    # Perform logical delete
    
    if request.method == 'GET':
        book = session.query(Books).filter(Books.id_==dataId).first()
        headers = ['Book title', 'Volume number', 'Author', 'Publisher', 'Memo']
        return template('confirm.html'
            , form=book_2_form(book)
            , headers=headers
            , registId=dataId)
    else:
        dataId = request.forms.decode().get('id')
        book = session.query(Books).filter(Books.id_==dataId).first()
        ic("FROM POST:", dataId)
        book.del_flag = 1
        session.commit()
        session.close()
    redirect('/list')

