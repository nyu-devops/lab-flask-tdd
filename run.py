"""
Pet Service Runner

Start the Pet Service and initializes logging
"""

import os
from app import app, service

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "****************************************"
    print " P E T   S E R V I C E   R U N N I N G"
    print "****************************************"
    service.initialize_logging()
    service.init_db()  # make our sqlalchemy tables
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
