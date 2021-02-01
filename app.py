from flask import Flask, render_template, request, redirect, url_for, make_response, session
import yattag
import pdfkit
import os

app = Flask(__name__, template_folder='./frontend/templates', static_folder='./frontend/static')
app.secret_key = 'bhaisa'


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        session['user'] = request.form
        return redirect(url_for("user"))
    else:
        return render_template('index.html')


@app.route("/user")
def user():
    if 'user' in session:
        user = session['user']
        doc, tag, text = yattag.Doc().tagtext()
        with tag('h2', style="text-align: center;"):
            with tag('span', style="color: #ff0000;"):
                text('Hard Work of FATPANDA')

        with tag('hr'):
            text()

        with tag('h2', style='text-align: center;'):
            with tag('span', style='text-decoration: underline; color: #000080;'):
                with tag('strong'):
                    text(user["user_name"])
        with tag('h4', style="text-align: center;"):
            with tag('span', style="color: #008000;"):
                text('Progress Achieved')
        with tag('p'):
            with tag('strong'):
                with tag('span', style='color: #0000ff;'):
                    text(user['message'])
        temp = os.getcwd()
        html_string_file = os.path.join(temp, 'html_string.html')
        temp = doc.getvalue()
        with open(html_string_file, 'w', encoding='utf8') as html_write:
            html_write.write(temp)
        config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')

        pdf = pdfkit.from_string(temp, False, configuration=config)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response


if __name__ == '__main__':
    app.run()
