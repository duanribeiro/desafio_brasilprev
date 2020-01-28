# -*- coding: latin-1 -*-
from tests.test_fixtures import client

def test_basic(client):
    response = client.get('/api/game/')

    assert response.status_code == 200
    assert len(response.json.keys()) == 4
    assert len(response.json['Qual a porcentagem de vitorias por comportamento dos jogadores']) > 0
