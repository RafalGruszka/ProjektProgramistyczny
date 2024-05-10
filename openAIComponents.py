from openai import OpenAI
import json

# Parameters

place = "Jaworzno"
activity = "wspinaczka"  # trekking/wspinaczka


def tripProposition(place: str, activity: str) -> dict:
    api_key = ""
    organization = ""
    question = f"Zaproponuj miejsce do {activity} w okolicy {place}."

    client = OpenAI(api_key=api_key, organization=organization)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON with following attributes: number, place, proposition_details, distance, equipment, hardenes_level, coordinates.\n"
                           "Create three numbered propositions to consider for a user. \n"
                           "Each proposition should start from place name written in capital letters, then rest of proposition content.\n"
                           f"For each place estimate the distance in kilometers from {place} entered by the user.\n"
                           f"For each proposition recommend equipment necessary for {activity}.\n"
                           f"For each proposition estimate climbing hardenes level in range from 1 to 5.\n"
                           "Add coordinates for each proposed place."
                           "\nAnswer in Polish language."
            },
            {"role": "user", "content": question},
        ],
    )

    response_content = response.choices[0].message.content

    return response_content

#print(tripProposition(place, activity))