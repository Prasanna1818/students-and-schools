from flask import Flask, render_template, request
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    num_schools = 5
    return render_template('index.html', num_schools=num_schools)

@app.route('/visualize', methods=['POST'])
def visualize():
    schools_data = []

    # Validate form data
    if 'num_schools' not in request.form or not request.form['num_schools']:
        return "Number of schools is missing or empty.", 400

    try:
        num_schools = int(request.form['num_schools'])
    except ValueError:
        return "Number of schools must be an integer.", 400

    for i in range(1, num_schools + 1):
        school_name_key = f'school_name_{i}'
        num_students_key = f'num_students_{i}'

        if school_name_key not in request.form or num_students_key not in request.form:
            return f"Data for school {i} is missing.", 400

        school_name = request.form[school_name_key]

        try:
            num_students = int(request.form[num_students_key])
        except ValueError:
            return f"Number of students for school {i} must be an integer.", 400

        schools_data.append({'School': school_name, 'Number of Students': num_students})

    # Create a bar chart using Plotly
    fig = px.bar(schools_data, x='School', y='Number of Students', color='School')

    return render_template('visualization.html', plot=fig.to_html())

if __name__ == '__main__':
    app.run(debug=True)
