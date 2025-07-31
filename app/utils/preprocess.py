def clean_creations(creations):
    elements = creations['Creations']

    all_keys = [
        'AfishaPriority',
        'Genres',
        'Duration',
        'Rating',
        'KinoplanId',
        'Images',
        'ProductionYear',
        'Name',
        'AfishaCreationUrl',
        'Videos',
        'ReleaseDate',
        'ShortDescription',
        'Description',
        'AfishaId',
        'AgeRestriction',
        'AfishaClassId',
        'MainPhotoCrops',
        'Id',
        'Participants',
        'Country',
        'Type',
        'DurationDescription',
    ]

    need_keys = [
        'Id',
        'Type',
        'Name',
        'Genres',
        'Description',
        'Rating',
        'ReleaseDate',
        'AgeRestriction',
        'Country',
        'AfishaId',
        'AfishaCreationUrl',
    ]

    filtered = []
    for element in elements:
        filtered_element = {k: element[k] for k in need_keys if k in element}
        filtered.append(filtered_element)
    return filtered

