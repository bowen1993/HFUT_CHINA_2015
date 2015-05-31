from design.models import parts, team_parts, teams

def getApriorRecommend():
    result = {
        'isSuccessful' : True,
        'recommend_list': [
            {'part_id':98, 'part_name':'BBa_M39201', 'part_type':'T7'},
            {'part_id':144, 'part_name':'BBa_B0011', 'part_type':'T7'},
            {'part_id':145, 'part_name':'BBa_B0012', 'part_type':'T7'},
            {'part_id':146, 'part_name':'BBa_B0013', 'part_type':'T7'},
            {'part_id':147, 'part_name':'BBa_B0030', 'part_type':'T7'},
        ]
    }
    return result

def getMarkovRecommend():
    result = {
        'isSuccessful' : True,
        'recommend_list': [
            {'part_id':98, 'part_name':'BBa_M39201', 'index':0, 'part_type':'T7'},
            {'part_id':144, 'part_name':'BBa_B0011', 'index':1, 'part_type':'T7'},
            {'part_id':145, 'part_name':'BBa_B0012', 'index':2, 'part_type':'T7'},
            {'part_id':146, 'part_name':'BBa_B0013', 'index':3, 'part_type':'T7'},
            {'part_id':147, 'part_name':'BBa_B0030', 'index':4, 'part_type':'T7'},
        ]
    }
    return result