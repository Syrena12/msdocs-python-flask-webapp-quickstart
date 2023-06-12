import os
import csv
import pandas as pd
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)


app = Flask(__name__)

df = pd.read_csv('resources/people.csv')
# ,header=0,index_col=0)


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False

@app.route('/')
def index():
    img_url = url_for('static', filename='images/dar.jpg')
    print(df)
    return render_template('index3.html',img_url=img_url)

@app.route('/search_by_name', methods=['POST'])
def search_by_name():
    result = []
    name = request.form['Name']
    find=df[df['Name'] == name]
    if find.shape[0]>0:
        find['img_url']= '/static/images/'+find['Picture']
        result=find.to_dict(orient='records')
        # print("===========================")
        # print(type(result))
        # print(result)
    return render_template('result.html', result=result)

@app.route('/search_by_salary', methods=['POST'])
def search_by_salary():
    result = []
    start_salary = 0
    if is_number(request.form['End_salary']) :
        end_salary = float(request.form['End_salary'])
        if is_number(request.form['Start_salary']):
            start_salary = float(request.form['Start_salary'])
        for index,row in df.iterrows():
            print ('row Salary')
            print (type(row['Salary']))
            if is_number(row['Salary']):
                salary = float(row['Salary'])
                if start_salary <= salary <= end_salary:
                    row['img_url']= '/static/images/'+row['Picture']
                    result.append(row)
        return render_template('result.html', result=result)
    else:
        return 'Input Error'    

@app.route('/upload_zip', methods=['POST'])
def upload_zip():
    print('==================================')
    f = request.files['zipFile']
    print(type(f))
    pass


@app.route('/update_user', methods=['POST'])
def update_user():
    global df
    name = request.form['Name']
    state = request.form['State']
    salary = request.form['Salary']
    grade = request.form['Grade']
    room = request.form['Room']
    telnum = request.form['Telnum']
    keywords = request.form['Keywords']
    # picture = request.form['Picture']

    find=df[df['Name'] == name]
    if find.shape[0]>0:
        if state!='' :
            df.loc[df['Name']==name,'State']=state
        if salary!='':
            if is_number(salary):
                df.loc[df['Name']==name,'Salary']=salary
            else:
                return 'Update Salary Failed'
        if grade!='':
            if is_number(grade):
                df.loc[df['Name']==name,'Grade']=grade
            else:
                return 'Update Grade Failed'
        if room!='':
            if is_number(room):
                df.loc[df['Name']==name,'Room']=room
            else:
                return 'Update Room Failed'
        if telnum!='' :
            if is_number(telnum):
                df.loc[df['Name']==name,'Telnum']=telnum
            else:
                return 'Update Telnum Failed'
        if keywords!='':
            df.loc[df['Name']==name,'Keywords']=keywords
        return 'Update Success' 
    return 'Found No User'


@app.route('/delete_user', methods=['POST'])
def delete_user():
    global df
    name = request.form['Name']
    find=df[df['Name'] == name]
    if find.shape[0]>0:
        df.drop(find.index)
        return 'Delete User Success'
    return 'Delete User Failed'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8090)
