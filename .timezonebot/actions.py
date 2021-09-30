#This files contains your custom actions which can be used to run
#custom Python code.

#See this guide on how to implement these action:
#https://rasa.com/docs/rasa/core/actions/#custom-actions/


#This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import json
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# timezones = {
#     "London": "UTC +1:00",
#     "Sofia": "UTC +3:00",
#     "Lisbon": "UTC +1:00",
#     "Mumbai": "UTC +5:30"
# }



class ActionShowTimeZone(Action):

    def name(self) -> Text:
        return "action_show_time_zone"
        #must return the same name that is used in domain file

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, #get value of slots using tracker
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        #timezone = timezones.get(city)
        
        url = "https://www.amdoren.com/api/timezone.php"
        
        #param_dict = {'api_key':'MAMjpvRLtncF7JDNCUETkQ9JcJbWw7' , 'loc':city }

        timezone_api_call = requests.get(url,params={'api_key':'MAMjpvRLtncF7JDNCUETkQ9JcJbWw7',
                                                     'loc':str(city)})
        
        time_json = timezone_api_call.json()
        timezone = time_json['timezone']+" "+ str((int(time_json["offset"]) / 60.0))

        if timezone is None:
            output = "Could not find the time zone of {}".format(city)
        else:
            output = "Time zone of {} is {}".format(city,timezone)

        dispatcher.utter_message(text=output)
        # basically what is uttered back to the user

        return []
