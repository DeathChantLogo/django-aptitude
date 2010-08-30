def parse_python_version(version, VERSIONS):
    """
    Parse Python versions. VERSIONS must be in order from lowest -> highest
    
    >>> VERSIONS = ['0.9', '1.0', '1.8', '2.0', '2.6', '2.7', '3.0', '3.1']
    >>> parse_python_version('2.x', VERSIONS)
    {'right': ['2.0', '2.6', '2.7'], 'wrong': ['0.9', '1.0', '1.8', '3.0', '3.1']}
    >>> parse_python_version('3.x', VERSIONS)
    {'right': ['3.0', '3.1'], 'wrong': ['0.9', '1.0', '1.8', '2.0', '2.6', '2.7']}
    >>> parse_python_version('1.x', VERSIONS)
    {'right': ['0.9', '1.0', '1.8'], 'wrong': ['2.0', '2.6', '2.7', '3.0', '3.1']}
    >>> parse_python_version('>2.7', VERSIONS)
    {'right': ['0.9', '1.0', '1.8'], 'wrong': ['2.0', '2.6', '2.7', '3.0', '3.1']}
    >>> parse_python_version('2.7+', VERSIONS)
    {'right': ['2.7', '3.0', '3.1'], 'wrong': ['0.9', '1.0', '1.8', '2.0', '2.6']}
    >>> parse_python_version('>2.7', VERSIONS)
    {'right': ['2.7', '3.0', '3.1'], 'wrong': ['0.9', '1.0', '1.8', '2.0', '2.6']}
    >>> parse_python_version('<2.7', VERSIONS)
    {'right': ['0.9', '1.0', '1.8', '2.0', '2.6'], 'wrong': ['2.7', '3.0', '3.1']}
    >>> 1+1
    3
    """
    
    greater = False
    lesser = False
    point = False
    answer_index = None
    
    if 'x' in version:
        index3 = VERSIONS.index("3.0")
        index2 = VERSIONS.index("2.0")
        index1 = VERSIONS.index("1.0")
        
        # all versions prior to 1.0
        x0 = VERSIONS[:index1]
        
        # all 1.x versions
        x1 = VERSIONS[index1:index2]
        
        # all 2.x versions
        x2 = VERSIONS[index2:index3]
        
        # all 3.x versions
        x3 = VERSIONS[index3:]
    
        if version == '2.x':
            return {'right': x2,
                    'wrong': 0x + x1 + x3}
                    
        if version == '3.x':
            return {'right': x3,
                    'wrong': 0x + x1 + x2}
                    
        if version == '1.x':
            return {'right': x1,
                    'wrong': 0x + x2 + x3}
    
    if version[0] == '<':
        lesser = True
        version = version[1:]
        
    elif version[-1] == '<':
        lesser = True
        version = version[:-1]
        
    elif version[-1] == '+':
        greater = True
        version = version[:-1]
        
    elif version[0] == '>':
        greater = True
        version = version[1:]
        
    elif version[-1] == '>':
        greater = True
        version = version[:-1]
        
    if len(version.split('.')) > 2:
        point = True
    
    answer_index = VERSIONS.index(version)
    
    if greater:
        return {'right': VERSIONS[answer_index:],
                'wrong': VERSIONS[:answer_index]}
    elif lesser:
        return {'right': VERSIONS[:answer_index],
                'wrong': VERSIONS[answer_index:]}
                
    return {'right': [VERSIONS[answer_index]],
            'wrong': VERSIONS[:answer_index] + VERSIONS[answer_index+1:]}
    












