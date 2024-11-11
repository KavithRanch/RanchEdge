from backend import app

# Checks if run.py file executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True)

