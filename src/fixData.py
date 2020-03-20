__author__ = "Rafael Machado"

import pandas as pd

confirmed = pd.read_csv('../data/confirmedGit.csv')

confirmed_fixes_dict = {'Italy|3/12/20': 15113,
                        'Spain|3/12/20': 3146,
                        'France|3/12/20': 2876,
                        'United Kingdom|3/12/20': 590,
                        'Germany|3/12/20': 2745,
                        'Argentina|3/12/20': 19,
                        'Australia|3/12/20': 122,
                        'Belgium|3/12/20': 314,
                        'Chile|3/12/20': 23,
                        'Colombia|3/12/20': 9,
                        'Greece|3/12/20': 98,
                        'Indonesia|3/12/20': 34,
                        'Ireland|3/12/20': 43,
                        'Japan|3/12/20': 620,
                        'Netherlands|3/12/20': 503,
                        'Qatar|3/12/20': 262,
                        'Singapore|3/12/20': 178,
                        'United Kingdom|3/15/20': 1391,
                        'France|3/15/20': 5423}
                        
#deaths_fixes_dict = {'Italy|3/12/20': 1016,
#                     'Spain|3/12/20': 86,
#                     'France|3/12/20': 61,
#                     'Germany|3/12/20': 6,
#                     'Argentina|3/12/20': 1,
#                     'Australia|3/12/20': 3,
#                     'Greece|3/12/20': 1,
#                     'Indonesia|3/12/20': 1,
#                     'Ireland|3/12/20': 1,
#                     'Japan|3/12/20': 15,
#                     'Netherlands|3/12/20': 5,
#                     'Switzerland|3/12/20': 4,
#                     'United Kingdom|3/15/20': 35,
#		              'France|3/15/20': 127}
                     
#recovered_fixes_dict = {'Italy|3/12/20': 1258,
#                        'Spain|3/12/20': 189,
#                        'France|3/12/20': 12,
#                        'Germany|3/12/20': 25}
#        

for key in confirmed_fixes_dict.keys():
    country_to_be_fixed = key.split('|')[0]
    date_to_be_fixed = key.split('|')[1]
    value_to_be_fixed = confirmed_fixes_dict[key]
    confirmed[date_to_be_fixed][confirmed['Country/Region'] == country_to_be_fixed] = value_to_be_fixed
        
confirmed.to_csv('../data/confirmedFixed.csv')

#for key in deaths_fixes_dict.keys():
#    country_to_be_fixed = key.split('|')[0]
#    date_to_be_fixed = key.split('|')[1]
#    value_to_be_fixed = fixes_dict[key]
#    dataframe_deaths_DF.at[country_to_be_fixed, date_to_be_fixed] = value_to_be_fixed
        

#for key in recovered_fixes_dict.keys():
#    country_to_be_fixed = key.split('|')[0]
#    date_to_be_fixed = key.split('|')[1]
#    value_to_be_fixed = fixes_dict[key]
#    dataframe_recovered_DF.at[country_to_be_fixed, date_to_be_fixed] = value_to_be_fixed