from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Months List:
months = [ "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December" ]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        month = request.form.get('month')
        day = request.form.get('day')
        try:
            month_num = datetime.strptime(month, "%B").month
            lmp_date = datetime.strptime(f"2025-{month_num}-{int(day)}", "%Y-%m-%d")
            ovulation_day = lmp_date + timedelta(days=14)
            fertile_window = f"{(ovulation_day - timedelta(days=5)).strftime('%b %d')} - {(ovulation_day + timedelta(days=1)).strftime('%b %d')}"
            result = {
                "Ovulation Day": ovulation_day.strftime('%b %d'),
                "Fertile Window": fertile_window
            }
        except:
            result = "Invalid Input"

    return render_template('index.html', months=months, result=result)
