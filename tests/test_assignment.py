from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

import main


SAMPLE = Path(__file__).resolve().parents[1] / 'player.csv'


def test_sample_participants_are_assigned_once_with_group_separation():
    participants = pd.read_csv(SAMPLE).to_dict(orient='records')
    teams = main.compute_teams(participants, 2)
    members = [member for team in teams for member in team['members']]
    expected = {person['이름'] for person in participants if person['참가여부']}
    assert len(members) == len(expected) == 8
    assert {person['이름'] for person in members} == expected
    for group in ['A', 'B']:
        assert all(sum(person.get('분리그룹') == group for person in team['members']) <= 1 for team in teams)
    assert all(team['male'] + team['female'] == team['total'] for team in teams)


def test_upload_redirects_to_result_and_edit_screen():
    main.results_cache.clear()
    try:
        with TestClient(main.app) as client:
            assert client.get('/').status_code == 200
            response = client.post('/assign',
                files={'file': ('example.csv', SAMPLE.read_bytes(), 'text/csv')},
                data={'team_count': '2'}, follow_redirects=False)
            assert response.status_code == 303
            result_url = response.headers['location']
            assert result_url.startswith('/result/')
            assert client.get(result_url).status_code == 200
            token = result_url.rsplit('/', 1)[1]
            assert client.get('/edit/' + token).status_code == 200
            assert len(main.results_cache[token]['participants']) == 10
    finally:
        main.results_cache.clear()
