import os

from laptoplib import app

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT") or 5000)