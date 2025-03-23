from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

# List of months to pass to template
months = [ "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December" ]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        month = request.form.get('month')
        day = request.form.get('day')
        try:
            # Convert month name to number
            month_num = datetime.strptime(month, "%B").month
            # Get year (current year)
            year = datetime.now().year
            # Create date object from input
            lmp_date = datetime.strptime(f"{year}-{month_num}-{int(day)}", "%Y-%m-%d")

            # Predict ovulation (14 days before next period, assuming 28-day cycle)
            cycle_length = 28
            ovulation_day = lmp_date + timedelta(days=(cycle_length - 14))
            fertile_start = ovulation_day - timedelta(days=5)
            fertile_end = ovulation_day + timedelta(days=1)
            next_period = lmp_date + timedelta(days=cycle_length)

            result = {
                "Ovulation Day": ovulation_day.strftime('%b %d'),
                "Fertile Window": f"{fertile_start.strftime('%b %d')} - {fertile_end.strftime('%b %d')}",
                "Next Period": next_period.strftime('%b %d'),
                # Best days to spit game: day before ovulation & ovulation day
                "Prime Time": f"{(ovulation_day - timedelta(days=1)).strftime('%b %d')} & {ovulation_day.strftime('%b %d')}"
            }
        except:
            result = "Invalid Input"

    return render_template('index.html', months=months, result=result)

if __name__ == '__main__':
    app.run(debug=True)
