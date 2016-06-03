"""Main executable script for recipeshelf site
Calls functions from the views module, which handles routing"""
from recipeshelf.views import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
