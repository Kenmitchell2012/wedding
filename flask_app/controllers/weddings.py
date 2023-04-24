from flask_app import app
from flask import render_template, redirect, url_for, request, flash, session
from flask_app.models.user import User
from flask_app.models.wedding import Wedding


# new wedding page
@app.route('/create')
def create_wedding_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    return render_template('create.html', user=user)



# Create a wedding  
@app.route('/create/wedding', methods=['POST'])
def create_wedding():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print(session['user_id'])
    if not Wedding.validate_wedding(request.form):
        return redirect('/create')
    new_wedding = {
        'user_id': session['user_id'],
        # get creator name
        'creator': session['user_id'],
        'wedding_side': request.form['wedding_side'],
        'meal': request.form['meal'],
        'drink': request.form['drink'],
        'favorite_memory': request.form['favorite_memory']
    }
    print(new_wedding)
    Wedding.save_wedding(new_wedding)
    return redirect(url_for('dashboard'))

# view a wedding
@app.route('/wedding/view/<int:id>')
def view_wedding(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    wedding = Wedding.get_wedding_by_id(id)
    return render_template('view.html', user=user, wedding=wedding)

# edit wedding
@app.route('/wedding/edit/<int:wedding_id>')
def edit_wedding(wedding_id):
    if 'user_id' not in session:
        return redirect('/login')
    user = User.get_by_id(session['user_id'])
    wedding = Wedding.get_wedding_by_id(wedding_id)
    return render_template('edit.html', wedding=wedding, user=user)

# delete a wedding
@app.route('/wedding/delete/<int:id>')
def delete_wedding(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Wedding.delete({'id':id})
    return redirect('/dashboard')