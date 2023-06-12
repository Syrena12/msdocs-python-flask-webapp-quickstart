import os
import csv
import pandas as pd
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)


app = Flask(__name__)

@app.route('/')
def index():
    img_url = url_for('static', filename='images/cat.jpg')
    return render_template('index3.html',img_url=img_url)

data = []
with open('resources/q0c.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

@app.route('/search_by_room', methods=['POST'])
def search_by_room():
    img_path = ''
    room = request.form['room']
    result = []
    for row in data:
        if row['room'] == room:
            result.append(row)
            img_path = row['pic']
            break
    if img_path:
        img_url = url_for('static', filename='images/'+img_path)
    else:
        img_url = 'no information or picture available'

    return render_template('search_by_room.html', result=result,img_url=img_url)

@app.route('/search_by_teln', methods=['POST'])   #好像是坏的
def search_by_teln():
    start_teln = 0
    if request.form['start_teln'].isdigit():
        start_teln = int(request.form['start_teln'])
    end_teln = int(request.form['end_teln'])
    result = []
    img_path=''
    for row in data:
        if row['teln'].isdigit():
            teln = int(row['teln'])
            if start_teln <= teln <= end_teln:
                img_path = row['pic']
                if img_path:
                    row['pic'] = url_for('static', filename='images/'+img_path)
                else:
                    row['pic'] = 'no information or picture available'
                result.append(row)
    if len(result)==0:
        row={'name':'no information or picture available'}
        result.append(row)
    return render_template('search_by_teln.html', result=result)

# @app.route('/update_description', methods=['POST'])
# def update_description():
#     teln = request.form['teln']
    
#     new_description = request.form['new_description']
#     message='Teln number not found.'
#     for row in data:
#         if row['Telnum'] == teln:
#             row['descript'] = new_description
#             # 怎么save到csv里
            
#             # # path为输出路径和文件名，newline=''是为了不出现空行
#             # csvFile = open('resources/temp.csv', "w+",newline='')
#             # try:
#             #     # data为list类型
#             #     for i in range(len(data)):
#             #         writer.writerow(data[i])
#             # finally:
#             #     csvFile.close()


#             ##################
#             message= 'Description updated successfully!'
#             break
#     return render_template('update_description.html', message=message)
    




#================================================================================================================================


# filename = 'resources/q0c.csv'  # 修改为 csv 文件路径
# img_dir = 'resources/'  # 修改为图片路径


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     img_path = ''
#     if request.method == 'POST':
#         search = request.form.get('search')
#         with open(filename, newline='') as f:
#             reader = csv.reader(f)
#             next(reader)
#             for row in reader:
#                 if search == row[0]:
#                     img_path = row[2]
#                     break
#         if img_path:
#             img_url = url_for('img_file', filename=img_path)
#         else:
#             img_url = url_for('static', filename='images/cat.jpg')
#     else:
#         img_url = url_for('static', filename='images/cat.jpg')
#     table = read_csv_table()
#     return render_template('index2.html', table=table, img_url=img_url)


# @app.route('/img_file/<filename>')
# def img_file(filename):
#     return send_from_directory(img_dir, filename)


# def read_csv_table():
#     with open(filename, newline='') as f:
#         reader = csv.reader(f)
#         next(reader)
#         table = [{'name': row[0], 'room': row[1], 'pic': row[2],'teln':row[3],'descript':row[4]} for row in reader]
#     return table


#================================================================================================================================


# @app.route('/')
# def index():
#    print('Request for index page received')
#    return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

# @app.route('/hello', methods=['POST'])
# def hello():
#    name = request.form.get('name')

#    if name:
#        print('Request for hello page received with name=%s' % name)
#        return render_template('hello.html', name = name)
#    else:
#        print('Request for hello page received with no name or blank name -- redirecting')
#        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8090)
