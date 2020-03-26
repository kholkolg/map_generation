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
    if rule[0] == 0:
        suggestions = grid(vertex, rule[2])

    #Organic
    if rule[0] == 1:
        suggestions = organic(vertex, rule[2])

    #Radial
    if rule[0] == 2:
        suggestions = radial(rule[1], vertex, rule[2])

    #minor_road
    if rule[0] == 3:
        suggestions = minor_road(vertex, rule[2])
    #seed
    if rule[0] == 4:
        suggestions = seed(vertex, rule[2])

    # print('suggestions ', suggestions)
    return suggestions
