# -*- coding: utf-8 -*-
from proc_model.getRule import getRule
from proc_model.growth_rules.grid import grid
from proc_model.growth_rules.organic import organic
from proc_model.growth_rules.radial import radial
from proc_model.growth_rules.seed import seed
from proc_model.growth_rules.minor_road import minor_road


def getSuggestion(vertex):
    """
    Calls each of the actual growth rules, and returns a list of suggested vertices

    Parameters
    ----------
    vertex : Vertex object

    Returns
    -------
    list<Vertex>


    """
    # print('suggestion ', vertex)
    suggestions=[]
    rule= getRule(vertex)
    #Grid
    # if rule[0] == 0:
    l=grid(vertex, rule[2])
    for x in l:
        # print('grid ',x)
        # if x != vertex:
        #     print('append')
            suggestions.append(x)
    # #Organic
    if rule[0] == 1:

        l=organic(vertex, rule[2])
        for x in l:
            # print('organic ', x)
            # if x != vertex:
            #     print('append')
                suggestions.append(x)
    #Radial
    if rule[0] == 2:

        l=radial(rule[1], vertex, rule[2])
        for x in l:
            # print('radial ', x)
            # if x != vertex:
            #     print('append')
                suggestions.append(x)
    #minor_road
    if rule[0] == 3:
        l=minor_road(vertex, rule[2])
        for x in l:
            # print('minor ', x)
            # if x != vertex:
            #     print('append')
                suggestions.append(x)
    #seed
    if rule[0] == 4:
        l=seed(vertex, rule[2])
        for x in l:
            # print('seed ', x)
            # if x != vertex:
            #     print('append')
                suggestions.append(x)

    # print('suggestions ', suggestions)
    return suggestions
