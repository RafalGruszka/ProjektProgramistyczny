from openai import OpenAI
import json


def tripProposition(place: str, activity: str) -> json:
    api_key = "" # API key
    organization = ""   # Organization ID
    question = f"Zaproponuj miejsce do {activity} w okolicy {place}."

    client = OpenAI(api_key=api_key, organization=organization)

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON response.\n"
            "Create three trip proposition in following json format:"
        "{'trip_propositions': [   \n" 
                "{ \n" 
                    "'number': 1,\n"
                    "'place': <place in capital letters>,\n"
		            "'proposition_details': <place description with at least 100 words>,\n"
    		        "'distance': <distance in km>, \n"
        		    "'equipment': <necessary equipment>, \n"
		            "'hardenes_level': <hardenes level in range 1 to 5>, \n"
		            "'coordinates': \n"
			            "{ \n"
    			            "'latitude': 49.5736, \n"
	    		            "'longitude': 19.5731 \n"
    		        	"} \n"
	    	    "}, \n"
		        "{ \n"
                    "'number': 2, \n"
                    "'place': <place in capital letters>, \n"
                    "'proposition_details': <place description with at least 100 words>, \n"
                    "'distance': <distance in km>, \n"
                    "'equipment': <necessary equipment>, \n"
                    "'hardenes_level': <hardenes level in range 1 to 5>, \n"
                    "'coordinates': \n"
                        "{ \n" 
                         "'latitude': 49.5736, \n"
                         "'longitude': 19.5731 \n"
                        "} \n"
                "}, \n"
                "{ \n"
                    "'number': 3, \n"
                    "'place': <place in capital letters>, \n"       
                    "'proposition_details': <place description with at least 100 words>, \n"
                    "'distance': <distance in km>, \n"
                    "'equipment': <necessary equipment>, \n"
                    "'hardenes_level': <hardenes level in range 1 to 5>, \n"
                    "'coordinates': \n"
                        "{ \n"
                         "'latitude': 49.5736, \n"
                         "'longitude': 19.5731 \n"
                        "} \n"
                "} \n"
            "] \n"
        "}  \n"
                                  "Each proposition should start from place name written in capital letters, then rest of proposition content.\n"
                                  f"For each place estimate the distance in kilometers from {place} .\n"
                                  f"For each proposition recommend equipment necessary for {activity}.\n"
                                  f"<proposition_details> JSON atttribute as a place description should contain about 300 words.\n"
                                  "\nAnswer in Polish language."},
        {"role": "user", "content": question}
    ]
    )
    return response.choices[0].message.content

# Parameters

# Test API request
#place = "Jaworzno"
#activity = "trekking"  # trekking/wspinaczka
#x = tripProposition(place, activity)
#print(type(x))
#print(x)





