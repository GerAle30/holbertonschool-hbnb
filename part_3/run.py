from app import create_app, db

app = create_app()

@app.before_first_request
def create_tables():
    """Create database tables before first request"""
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5001)
