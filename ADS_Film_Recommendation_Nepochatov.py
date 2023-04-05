import math as m
import numpy as np


'''
Final project ADS2 "Film Recommendation" by Alexey Nepochatov.

Description of the algorithm:

The structure of the input data allows us to use graph theory, 
i.e. we will represent our data as a graph, 
where films are vertices and similarities are edges. 
Since there is no necessary condition that there is a similarity 
between each pair of films, the graph may consist of several non-connected components,
where each component is a group of similar films.

We will present our data in the form of a adjacency list.
For this we will go through the [similarities] and create an adjacency list,
where vertices are films. Then we will store it as a dictionary {film_features},
where keys are films and values will be features of each film, like similar (adjacency) films.

Then, using Depth-first search algorithm we will go through [movies],
which are the vertices of the graph and create a list of related movies.

Then, we will calculate the number of friends who have seen the film (discussability).

Finally, we will go through the list of non-connected components and for each component
find number of friends who watched films of this component, and for each
film find the number of friends who watched this film, then find
mean number of friends who watched similar films.
Using this data we will find score for each film and return film with the highest score.
'''


# Depth-first search
def dfs(film, film_features, related_films, visited):
    visited[film] = True
    related_films.add(film)

    if film_features[film] is not None:
        for adjacency_film in film_features[film]['adjacency films']:
            if adjacency_film not in visited:
                dfs(adjacency_film, film_features, related_films, visited)

    return related_films


def film_recommendation(movies, similarities, friends):
    film_to_recommend = None

    '''
    Go through the [similarities] and create an adjacency list,
    where nodes are films. Then store it as a dictionary,
    where keys are films and values are similar (adjacency) films.
    Time complexity O(Similarities) - we have one cycle by similarities.
    Space complexity O(Movies + Similarities) 
    '''
    film_features = dict.fromkeys(movies, None)

    for similar_films in similarities:
        first_film = similar_films[0]
        second_film = similar_films[1]

        if film_features[first_film] is None:
            film_features[first_film] = {'adjacency films': set()}
        if film_features[second_film] is None:
            film_features[second_film] = {'adjacency films': set()}

        film_features[first_film]['adjacency films'].add(second_film)
        film_features[second_film]['adjacency films'].add(first_film)

    '''
    Use DFS to go through [movies] and create a list of related movies:
    Time complexity O(Movies + Similarities)
    Space complexity O(2*Movies)
    '''

    visited = {}
    list_of_sets_of_similar_films = []

    for film in movies:
        if film not in visited:
            visited[film] = True
            related_films = dfs(film, film_features, set(), visited)
            list_of_sets_of_similar_films.append(related_films)

    '''
    Calculate the number of friends who have seen the film (discussability)
    Time complexity O(Movies * Friends)
    Space complexity O(Movies)
    '''

    for film in film_features:
        if film_features[film] is not None:
            if 'discussability' not in film_features[film]:
                film_features[film].update({'discussability': 0})

    for list_of_seen_films_by_friend in friends:
        for film in list_of_seen_films_by_friend:
            if film_features[film] is not None:
                film_features[film]['discussability'] += 1

    '''
    Go through the [list_of_sets_of_similar_films] and for each {set_of_similar_films}
    find number of friends who watched films of this set, and for each
    film find the number of friends who watched this film, then find
    mean number of friends who watched similar films.
    Using this find score for each film and return film with the highest_score.
    '''
    highest_score = -m.inf

    '''
    Time complexity O(movies)
    '''
    for set_of_similar_films in list_of_sets_of_similar_films:
        total_seen = 0
        number_of_similar_films = len(set_of_similar_films) - 1

        '''
        Calculate the number of friends who watched similar films
        Time complexity O(Friends)
        '''

        for film in set_of_similar_films:
            if film_features[film] is not None:
                total_seen += film_features[film]['discussability']

        '''
        Calculate the the score of film for each film
        Time complexity O(similarities)
        '''
        for film in set_of_similar_films:
            score_of_film = 0

            if film_features[film] is not None:
                discussability = film_features[film]['discussability']
            else:
                discussability = 0

            similar_seen = total_seen - discussability

            if similar_seen != 0:  # Exclude the films with S = 0
                mean = similar_seen / number_of_similar_films
                score_of_film = discussability / mean

                '''
                *** Check Block ***
                Contains Features of the film
                '''
                print("***Film***\n "
                      "name: {film}\n discussability: {d}"
                      "\n number of similar films: {s}"
                      "\n number friends seen similar films: {nf}"
                      "\n mean: {mean}"
                      "\n score: {sc}".format(
                                              film=film,
                                              d=discussability,
                                              s=number_of_similar_films,
                                              nf=similar_seen,
                                              mean=mean,
                                              sc=np.round_(score_of_film, decimals=3)
                                              ))
                '''
                *** End of Check Block ***
                '''
            if score_of_film > highest_score:  # find film with the highest_score
                film_to_recommend, highest_score = film, score_of_film

    '''
    In result:
    Time complexity of the algorithm is O(similarities + movies*friends)
    Space complexity of the algorithm is O(movies + similarities)
    '''
    return film_to_recommend


# Input ==========================================================

if __name__ == "__main__":
    # Base test
    movies = ["Parasite", "1917", "Ford v Ferrari", "Jojo Rabbit", "Joker"]
    similarities = [["Parasite", "1917"],
                    ["Parasite", "Jojo Rabbit"],
                    ["Joker", "Ford v Ferrari"]]
    friends = [["Joker"],
               ["Joker", "1917"],
               ["Joker"],
               ["Parasite"],
               ["1917"],
               ["Jojo Rabbit", "Joker"]]

    recommended = film_recommendation(movies, similarities, friends)
    print("Recommended:", recommended)

    # Test №1
    movies_1 = ["A", "B", "C", "D", "E", "F", "G", "H"]
    similarities_1 = [["A", "B"],
                      ["B", "C"],
                      ["D", "E"],
                      ["E", "G"],
                      ["B", "H"]]

    friends_1 = [["H"],
                 ["A"],
                 ["A", "B", "F", "G"],
                 ["A"],
                 ["B"],
                 ["D"],
                 ["D", "E"],
                 ["C", "H"],
                 ["C"],
                 ["H"]]

    # recommended = film_recommendation(movies_1, similarities_1, friends_1)
    # print("Recommended:", recommended)

    # Test №2
    movies_2 = ["A", "B", "C", "D", "E", "F", "G", "H"]
    similarities_2 = []

    friends_2 = [["H"],
                 ["A"],
                 ["A", "B", "F", "G"],
                 ["A"],
                 ["B"],
                 ["D"],
                 ["D", "E"],
                 ["C", "H"],
                 ["C"],
                 ["H"],
                 ["F"]]

    # recommended = film_recommendation(movies_2, similarities_2, friends_2)
    # print("Recommended:", recommended)

    # Test №3
    movies_3 = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    similarities_3 = [["A", "B"],
                      ["C", "D"],
                      ["E", "F"],
                      ["F", "G"],
                      ["H", "I"]]

    friends_3 = [["A"],
                 ["B"],
                 ["C"],
                 ["D"],
                 ["E"],
                 ["F"],
                 ["G"],
                 ["I"]]

    # recommended = film_recommendation(movies_3, similarities_3, friends_3)
    # print("Recommended:", recommended)
