import pandas as pd


# Normalizing the Oscars data
def normalize_oscars(df):
    df = df.replace({'category': {'ACTOR': 'lead_actor', 'ACTOR IN A LEADING ROLE': 'lead_actor',
                         'ACTRESS': 'lead_actress', 'ACTRESS IN A SUPPORTING ROLE': 'lead_actress',
                         'ACTRESS IN A SUPPORTING ROLE': 'supporting_actress', 
                         'ACTOR IN A SUPPORTING ROLE': 'supporting_actor',
                         'OUTSTANDING PICTURE': 'best_picture','OUTSTANDING PRODUCTION': 'best_picture', 
                         'OUTSTANDING MOTION PICTURE': 'best_picture', 'BEST MOTION PICTURE': 'best_picture', 
                         'BEST PICTURE': 'bset_picture'}})
    df1 = df[df.category == 'best_picture']
    df2 = df[df.category == 'lead_actor']
    df3 = df[df.category == 'lead_actress']
    df4 = df[df.category == 'supporting_actor']
    df5 = df[df.category == 'supporting_actress']
    df = pd.concat([df1, df2, df3, df4, df5])
    
    newlist = [[2018, 'best_picture', True, 'The Shape of Water'],
               [2018, 'best_picture', False, 'Call Me By Your Name'],
               [2018, 'best_picture', False, 'Darkest Hour'],
               [2018, 'best_picture', False, 'Dunkirk'],
               [2018, 'best_picture', False, 'Get Out'],
               [2018, 'best_picture', False, 'Lady Bird'],
               [2018, 'best_picture', False, 'Phantom Thread'],
               [2018, 'best_picture', False, 'The Post'],
               [2018, 'best_picture', False, 'Three Billbaords Outside of Ebbing, Missouri'],
               [2018, 'lead_actor', True, 'Gary Oldman'], 
               [2018, 'lead_actor', False, 'Timothee Chalamet'],
               [2018, 'lead_actor', False, 'Daniel Day-Lewis'],
               [2018, 'lead_actor', False, 'Daniel Kaluuya'],
               [2018, 'lead_actor', False, 'Danzel Washington'],
               [2018, 'lead_actress', True, 'Frances McDormand'], 
               [2018, 'lead_actress', False, 'Sally Hawkins'],
               [2018, 'lead_actress', False, 'Margot Robbie'],
               [2018, 'lead_actress', False, 'Saoirse Ronan'],
               [2018, 'lead_actress', False, 'Meryl Streep'],
               [2018, 'supporting_actor', True, 'Gary Oldman'], 
               [2018, 'supporting_actor', False, 'Timothee Chalamet'],
               [2018, 'supporting_actor', False, 'Daniel Day-Lewis'],
               [2018, 'supporting_actor', False, 'Daniel Kaluuya'],
               [2018, 'supporting_actor', False, 'Danzel Washington'],
               [2018, 'supporting_actress', True, 'Frances McDormand'], 
               [2018, 'supporting_actress', False, 'Sally Hawkins'],
               [2018, 'supporting_actress', False, 'Margot Robbie'],
               [2018, 'supporting_actress', False, 'Saoirse Ronan'],
               [2018, 'supporting_actress', False, 'Meryl Streep'],
               [2019, 'best_picture', True, 'Green Book'],
               [2019, 'best_picture', False, 'Black Panther'],
               [2019, 'best_picture', False, 'Blackkklansman'],
               [2019, 'best_picture', False, 'Bohemian Rhaspody'],
               [2019, 'best_picture', False, 'The Favourite'],
               [2019, 'best_picture', False, 'Roma'],
               [2019, 'best_picture', False, 'A Star Is Born'],
               [2019, 'best_picture', False, 'Vice'],
               [2019, 'lead_actor', True, 'Rami Malek'], 
               [2019, 'lead_actor', False, 'Christian Bale'],
               [2019, 'lead_actor', False, 'Bradley Cooper'],
               [2019, 'lead_actor', False, 'Willem Dafoe'],
               [2019, 'lead_actor', False, 'Viggo Mortensen'],
               [2019, 'lead_actress', True, 'Olivia Coleman'], 
               [2019, 'lead_actress', False, 'Yalitza Aparicio'],
               [2019, 'lead_actress', False, 'Glenn Close'],
               [2019, 'lead_actress', False, 'Lady Gaga'],
               [2019, 'lead_actress', False, 'Melissa McCarthy'],
               [2019, 'supporting_actor', True, 'Mahershala Ali'], 
               [2019, 'supporting_actor', False, 'Adam Driver'],
               [2019, 'supporting_actor', False, 'Sam Elliott'],
               [2019, 'supporting_actor', False, 'Richard E. Grant'],
               [2019, 'supporting_actor', False, 'Sam Rockwell'],
               [2019, 'supporting_actress', True, 'Regina King'], 
               [2019, 'supporting_actress', False, 'Amy Adams'],
               [2019, 'supporting_actress', False, 'Marina De Tavira'],
               [2019, 'supporting_actress', False, 'Emma Stone'],
               [2019, 'supporting_actress', False, 'Rachel Weisz'],
               [2020, 'best_picture', False, 'Ford V Ferrari'],
               [2020, 'best_picture', False, 'The Irishman'],
               [2020, 'best_picture', False, 'Jojo Rabbit'],
               [2020, 'best_picture', False, 'Joker'],
               [2020, 'best_picture', False, 'Little Woman'],
               [2020, 'best_picture', False, 'Marriage Story'],
               [2020, 'best_picture', False, '1917'],
               [2020, 'best_picture', False, 'Once Upon A Time In Hollywood'],
               [2020, 'best_picture', False, 'Parasite'],
               [2020, 'lead_actor', False, 'Antonio Banderas'], 
               [2020, 'lead_actor', False, 'Leonardo Dicaprio'],
               [2020, 'lead_actor', False, 'Adam Driver'],
               [2020, 'lead_actor', False, 'Joaquin Phoenix'],
               [2020, 'lead_actor', False, 'Jonathan Pryce'],
               [2020, 'lead_actress', False, 'Cynthia Erivo'], 
               [2020, 'lead_actress', False, 'Scarlett Johansson'],
               [2020, 'lead_actress', False, 'Saoirse Ronan'],
               [2020, 'lead_actress', False, 'Charlize Theron'],
               [2020, 'lead_actress', False, 'Renee Zellweger'],
               [2020, 'supporting_actor', False, 'Tom Hanks'], 
               [2020, 'supporting_actor', False, 'Anthony Hopkins'],
               [2020, 'supporting_actor', False, 'Al Pacino'],
               [2020, 'supporting_actor', False, 'Joe Pesci'],
               [2020, 'supporting_actor', False, 'Brad Pitt'],
               [2020, 'supporting_actress', False, 'Kathy Bates'], 
               [2020, 'supporting_actress', False, 'Laura Dern'],
               [2020, 'supporting_actress', False, 'Scarlett Johansson'],
               [2020, 'supporting_actress', False, 'Florence Pugh'],
               [2020, 'supporting_actress', False, 'Margot Robbie']]
    addition = pd.DataFrame(newlist, columns = ['year', 'category', 'winner', 'entity'])
    df = df.append(addition)
    
    df.entity = df.entity.str.lower()
    df = df.reset_index().drop(columns='index')
    df = df.rename(columns = {'winner':'oscar_wins', 'entity':'nominee'})
    df.year = df.year.astype(object)
    return df


# Normalize Baftas
