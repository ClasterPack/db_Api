import json
from datetime import datetime, timedelta


class Competitor:

    def __init__(self, firstname, surname, tryout_number, record):
        self.firstname = firstname
        self.surname = surname
        self.tryout_number = tryout_number
        self.record = timedelta(seconds=record)

    def __repr__(self):
        return repr((self.tryout_number, self.firstname, self.surname, self.record))


with open('competitors.json', 'r', encoding='utf-8') as competitors_file:
    competitors = json.load(competitors_file)


with open('results_RUN.txt', 'r', encoding='utf-8') as results_file:
    participants = []
    for line in results_file.readlines():
        number, stage, stage_time = line.rstrip().split(' ')
        name, surname = competitors[number]['Name'], competitors[number]['Surname']
        competitor = competitors[number]
        if stage == 'start':
            competitor.update({'start': stage_time})
        elif stage == 'finish':
            competitor.update({'finish': stage_time})
            finish = datetime.strptime(competitor['finish'], '%H:%M:%S,%f')
            start = datetime.strptime(competitor['start'], '%H:%M:%S,%f')

        if competitor.get('finish') and competitor.get('start'):
            record = (finish - start).total_seconds()
            participants.append(Competitor(name, surname, number, round(record, 2)))


participants = sorted(participants, key=lambda competitors_podium: competitors_podium.record)
for participant in participants:
    print(participant, participant.record)


