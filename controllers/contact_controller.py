from flask import render_template, request, flash, redirect, url_for
from models.message import Message
from models import db

def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_content = request.form.get('message')
        
        if not name or not email or not message_content:
            flash('All fields are required!', 'danger')
            
            # If using flash, we need to show it in the template.
            # Assuming the template doesn't have flash message block yet, I will add it later.
            return redirect(url_for('contact'))
            
        new_message = Message(name=name, email=email, message=message_content)
        
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html')
