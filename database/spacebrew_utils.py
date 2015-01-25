__author__ = 'marion'


def calculate_spacebrew_name(osc_path):
    spacebrew_name = osc_path.split('/')[-1]
    return disambiguate_name_collisions(spacebrew_name, osc_path)


def disambiguate_name_collisions(spacebrew_name, osc_path):
    if spacebrew_name == 'dropped_samples':
        return osc_path.split('/')[-2] + '_' + osc_path.split('/')[-1]
    else:
        return spacebrew_name