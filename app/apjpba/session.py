import datetime
import json
from users.models import Session as Sess

class Session:
    def __init__(self, session_name):
        self.session_name = session_name
        
        data = Sess.objects.get(session_name=self.session_name)
        
        now = datetime.datetime.now()
        
        twenty_minutes_ago = now - datetime.timedelta(hours=2,minutes=20)
        
        if data.last_check > twenty_minutes_ago:
            self.data = data
            
            self.array = json.loads(data.session_data)
            
        return None
    
    def get(self, name):
        if name in self.array:
            return self.array[name]
        else:
            return None

