#### this was a way to enter BLS data at the command line. however this is inefficient. as i was getting ready to use this tool to import BLS data into the database,
#### i found a better way; parsing whole text files from BLS.  this will be implemented in a separate script.
import pandas as pd
import psycopg2

### collect data from the command line input

dataToAppend = []
state=True

while(state):

    seriesId = ''
    while (seriesId==''):
        seriesId=input("\n\nEnter the series id, q to quit: ")

    if seriesId == 'q':
        print('\n\nDone with entry tasks')
        state=False

    else:
        seriesTitle = ''
        while seriesTitle == '':
            seriesTitle = input("Enter the Series Title: ")

        if seriesTitle == 'q': 
            print('\n\nDone with entry tasks; the previous series Id will not be entered into data')
        
        else:
            print('\n\nSeries id: '+seriesId+'\n\nSeries title: '+seriesTitle+'\n\n')
            check=''
            while (check != 'y' and check != 'n'): 
                check=input('Is this correct y/n?')

            if check == 'y':
                seriesTuple=(seriesId, seriesTitle)
                dataToAppend.append(seriesTuple)
                seriesTitle = ''
                seriesId = ''
            
            elif check =='n':
                seriesTitle=''
                seriesId =''
                print('\n\nReenter series id and title')

            else:
                seriesTitle=''
                seriesId=''

print(dataToAppend)

conn = psycopg2.connect(
    host="localhost",
    port='5432',
    user='postgres',
    password='b13b3rh4u53',
    database='BLSdata'
)

cursor = conn.cursor()

for item in dataToAppend:

    query = 'INSERT INTO public.\"timeSeriesLabels\"(\"seriesId\", \"seriesTitle\")VALUES'+str(item)

    # Execute the query
    cursor.execute(query)

   # rows = cursor.fetchall()

   # print(rows)

#query = 'SELECT * FROM public.\"timeSeriesLabels\"'

cursor.close()
conn.close()