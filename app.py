from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Replace the hardcoded secret key with this

# Initialize Supabase client
supabase = create_client(
    supabase_url=os.getenv('SUPABASE_URL'),
    supabase_key=os.getenv('SUPABASE_KEY')
)

@app.route('/')
def index():
    # Fetch all employees
    response = supabase.table('employees').select("*").execute()
    employees = response.data
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        emp_id = request.form['emp_id']
        name = request.form['name']
        mobile = request.form['mobile']
        
        try:
            # Insert new employee
            data = supabase.table('employees').insert({
                "emp_id": emp_id,
                "name": name,
                "mobile": mobile
            }).execute()
            
            flash('Employee added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding employee: {str(e)}', 'error')
            
    return render_template('add.html')

@app.route('/edit/<string:emp_id>', methods=['GET', 'POST'])
def edit(emp_id):
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        mobile = request.form['mobile']
        
        try:
            # Update employee
            data = supabase.table('employees').update({
                "name": name,
                "mobile": mobile
            }).eq("emp_id", emp_id).execute()
            
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating employee: {str(e)}', 'error')
    
    # Get employee data for editing
    response = supabase.table('employees').select("*").eq("emp_id", emp_id).execute()
    employee = response.data[0] if response.data else None
    
    return render_template('edit.html', employee=employee)

@app.route('/delete/<string:emp_id>')
def delete(emp_id):
    try:
        # Delete employee
        supabase.table('employees').delete().eq("emp_id", emp_id).execute()
        flash('Employee deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting employee: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 