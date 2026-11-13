"""Validate the project metro topology using only the Python standard library."""

import json
from collections import defaultdict
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def reachable(start, adjacency):
    seen = {start}
    pending = [start]
    while pending:
        for neighbor in adjacency[pending.pop()]:
            if neighbor not in seen:
                seen.add(neighbor)
                pending.append(neighbor)
    return seen


def main():
    root = Path(__file__).resolve().parent
    stops = json.loads((root / 'metro-stops.json').read_text(encoding='utf-8'))
    lines = json.loads((root / 'metro-lines.json').read_text(encoding='utf-8'))
    ids = {stop['id']: stop for stop in stops}
    names = {stop['name']: stop['id'] for stop in stops}
    catalog = {line['id']: line for line in lines}
    require(len(ids) == len(stops), 'Duplicate station IDs')
    require(len(names) == len(stops), 'Duplicate station names')
    require(len(catalog) == len(lines), 'Duplicate line IDs')
    expected_counts = {'1': 25, '2': 25, '3': 25, '3bis': 4, '4': 29,
                       '5': 22, '6': 28, '7': 38, '7bis': 8, '8': 38,
                       '9': 37, '10': 23, '11': 19, '12': 31, '13': 32, '14': 21}
    metro = [line for line in lines if line['mode'] == 'metro']
    require({line['number'] for line in metro} == set(expected_counts), 'Incorrect metro lines')
    all_routes = {}
    all_memberships = set()
    graph, reverse_graph = defaultdict(set), defaultdict(set)
    metro_stations = set()
    connection_count = 0
    for line in metro:
        lid = line['id']
        vertices = set()
        route_pairs = defaultdict(set)
        for route in line['routes']:
            require(route['id'] not in all_routes, 'Duplicate route ID')
            all_routes[route['id']] = (lid, route)
            seq = route['station_ids']
            require(len(seq) >= 2 and all(s in ids for s in seq), f'Invalid route {route["id"]}')
            require(seq[0] == route['origin'] and seq[-1] == route['destination'], 'Invalid route terminals')
            vertices.update(seq)
            for position, sid in enumerate(seq, 1):
                all_memberships.add((sid, lid, route['id'], position))
            for a, b in zip(seq, seq[1:]):
                require(a != b, 'Self connection')
                route_pairs[(a, b)].add(route['id'])
        pairs = {(edge['source'], edge['target']) for edge in line['connections']}
        require(len(pairs) == len(line['connections']), f'Duplicate connections in {lid}')
        require(pairs == set(route_pairs), f'Connections disagree with routes in {lid}')
        require(len(vertices) == expected_counts[line['number']] == line['station_count'], f'Station count in {lid}')
        local, local_reverse, undirected = defaultdict(set), defaultdict(set), defaultdict(set)
        for edge in line['connections']:
            a, b = edge['source'], edge['target']
            require(set(edge['routes']) == route_pairs[(a, b)], 'Connection route references')
            require(edge['segment_id'] == f'{lid}:{min(a,b)}-{max(a,b)}', 'Invalid segment ID')
            time = edge['travel_time_minutes']
            require(time is None or (type(time) in (int, float) and time > 0), 'Invalid travel time')
            local[a].add(b)
            local_reverse[b].add(a)
            undirected[a].add(b)
            undirected[b].add(a)
            graph[a].add(b)
            reverse_graph[b].add(a)
        start = next(iter(vertices))
        require(reachable(start, local) == vertices and reachable(start, local_reverse) == vertices,
                f'Disconnected directed line {lid}')
        if line['number'] in ('7', '13'):
            branch = names['Maison Blanche' if line['number'] == '7' else 'La Fourche']
            require(line['branch_point'] == branch, 'Wrong branch point')
            require({v for v in vertices if len(undirected[v]) == 3} == {branch}, 'Invalid branch topology')
            require(sum(len(undirected[v]) == 1 for v in vertices) == 3, 'Expected three branch terminals')
        if line['topology'] == 'linear':
            require(all((b, a) in pairs for a, b in pairs), f'Missing reverse edge in {lid}')
            seq = line['routes'][0]['station_ids']
            for pos, sid in enumerate(seq, 1):
                membership = next(m for m in ids[sid]['lines'] if m['line'] == lid)
                require(membership['position'] == pos, f'Wrong position in {lid}')
        if line['number'] in ('7bis', '10'):
            directed_segments = (
                [('Botzaris', 'Place des Fêtes'), ('Place des Fêtes', 'Pré-Saint-Gervais'),
                 ('Pré-Saint-Gervais', 'Danube'), ('Danube', 'Botzaris')]
                if line['number'] == '7bis' else
                [('Boulogne - Jean Jaurès', 'Michel-Ange - Molitor'),
                 ('Michel-Ange - Molitor', 'Chardon Lagache'), ('Chardon Lagache', 'Mirabeau'),
                 ('Mirabeau', 'Javel - André Citroën'), ('Javel - André Citroën', "Église d'Auteuil"),
                 ("Église d'Auteuil", 'Michel-Ange - Auteuil'),
                 ('Michel-Ange - Auteuil', "Porte d'Auteuil"),
                 ("Porte d'Auteuil", 'Boulogne - Jean Jaurès')])
            for source, target in directed_segments:
                a, b = names[source], names[target]
                require((a, b) in pairs and (b, a) not in pairs, f'Wrong one-way segment: {source} -> {target}')
        metro_stations.update(vertices)
        connection_count += len(pairs)
    observed = set()
    for stop in stops:
        require(len({m['line'] for m in stop['lines']}) == len(stop['lines']), 'Duplicate station membership')
        for membership in stop['lines']:
            lid = membership['line']
            require(lid in catalog, f'Unknown line {lid}')
            if catalog[lid]['mode'] != 'metro':
                continue
            if catalog[lid]['topology'] != 'linear':
                require(membership['position'] is None, 'Ambiguous global position on a complex line')
            for position in membership['positions']:
                observed.add((stop['id'], lid, position['route'], position['position']))
    require(observed == all_memberships, 'Station memberships disagree with routes')
    require(len(metro_stations) == 321, 'Expected 321 metro stations')
    require(len(all_memberships) > 0, 'Missing memberships')
    start = next(iter(metro_stations))
    require(reachable(start, graph) == metro_stations and reachable(start, reverse_graph) == metro_stations,
            'Metro graph is not strongly connected')
    print(f'OK: {len(metro)} lines, {len(metro_stations)} metro stations, '
          f'{sum(l["station_count"] for l in metro)} station-line memberships, '
          f'{connection_count} directed connections, {len(all_routes)} routes.')
    print('OK: branch points, one-way segments, positions, references and directed connectivity.')
    print('Pending coordinates:', sum(s['coordinate_status'] == 'pending' for s in stops))


if __name__ == '__main__':
    main()
