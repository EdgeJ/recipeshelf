#!/usr/bin/env python2
"""
Main executable script for recipeshelf site
Calls functions from the views module, which handles routing.
"""
from recipeshelf.views import APP

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8080, debug=True)
