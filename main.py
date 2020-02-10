from flask import Flask
from flask import render_template
import pygal
import psycopg2

app = Flask(__name__)

"route binds app to an end point and 2.creates a path for the function"


@app.route('/index')
def index():
    conn=psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='Maldini'")

    cur = conn.cursor()


    data = [('internet Explorer', 19.5),('Firefox', 36.6),('Chrome', 36.3),('Safari', 4.5),('Opera', 2.3)]

    pie_chart = pygal.Pie() #instanciate
    pie_chart.title = 'Browser usage in February 2012 (in %)'
    pie_chart.add(data[0][0], data[0][1])
    pie_chart.add(data[1][0], data[1][1])
    pie_chart.add(data[2][0], data[2][1])
    pie_chart.add(data[3][0], data[3][1])
    pie_chart.add(data[4][0], data[4][1])

    pie_data=pie_chart.render_data_uri()


    line_data = [('January',20),
                 ('February', 12),
                 ('March', 45),
                 ('April', 56),
                 ('May', 65),
                 ('June', 67),
                 ('July', 89),
                 ('August', 98),
                 ('September', 100),
                 ('October', 96),
                 ('November', 54),
                 ('December', 45)
                 ]

    cur.execute("""SELECT EXTRACT (MONTHS FROM sales_data.created_at) AS months,
    SUM(sales_data.quantity) as "Total Sales" 
    FROM public.sales_data 
    GROUP BY 
    months 
    ORDER BY 
    months""")

    records = cur.fetchall()

    months = []
    sales = []
    for i in records:
        months.append(i[0])
        sales.append(i[1])
    print(months)
    print(sales)

    line_data = pygal.Line()
    line_data.title = "Sales made in the year 2015"
    line_data.x_labels = months
    line_data.add('Sale', sales)
    line_graph=line_data.render_data_uri()

    return render_template('index.html', pie_data=pie_data,line_graph=line_graph)


@app.route('/about')
def about():



    return render_template('about.html')

    #
    # browser =pygal.Line()
    # browser.title = "Change of programming languages over the years"
    # browser.x_lables = ['2011','2012','2013','2014','2015','2016']
    # browser.add('Python',[15,31,200,350,960])
    # browser.add('Java',[15,45,76,91,96])
    # browser.add('C++',[5,51,54,102,150,201])
    # browser.add('All Others',[5,15,12,55,92,105])
    # line_graph=browser.render_data_uri()

    # return render_template('about.html', line_graph=line_graph)

@app.route('/contact')
def contact():
    return render_template('contacts.html', title='My contacts')

@app.route('/service')
def service():
    return render_template('service.html')

if __name__ == '__main__':
    app.run()
    debug = True
