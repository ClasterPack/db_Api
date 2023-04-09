import json
from datetime import datetime
from competitor import Competitor

with open('competitors.json', 'r', encoding='utf-8') as competitors_file:
    competitors = json.load(competitors_file)


with open('results_RUN.txt', 'r', encoding='utf-8') as results_file:
    participants = []
    for line in results_file.readlines():
        number, stage, stage_time = line.rstrip().split(' ')
        competitor = competitors[number]
        stage_time = datetime.strptime(stage_time, '%H:%M:%S,%f')
        if stage == 'start':
            competitor.update({'start': stage_time})
        elif stage == 'finish':
            competitor.update({'finish': stage_time})
        if competitor.get('finish') and competitor.get('start'):
            name, surname = competitor['Name'], competitor['Surname']
            record = round((competitor['finish'] - competitor['start']).total_seconds(), 2)
            participants.append(
                Competitor(
                    competitors[number]['Name'],
                    competitors[number]['Surname'],
                    number,
                    record,
                )
            )

if __name__ == "__main__":
    participants = sorted(participants, key=lambda competitors_podium: competitors_podium.record)
    for position, participant in enumerate(participants):
        print(
            position+1,
            participant.tryout_number,
            participant.firstname,
            participant.surname,
            participant.record,
        )


