import pandas as pd



def main():
    filepath = 'dat/whole_set.csv'
    df = pd.read_csv(filepath)
    ## filter foreman
    print(df.columns)

    print(list(set(df.Role.values)))
    print(df.shape)


    query = ['formand', 'midlertidig formand']
    for term in query: 
        idx = df.Role.values != term
        df = df.loc[idx, :]
    
    print(list(set(df.Role.values)))
    print(df.shape)
    subject = df['Subject 1'].values
    time = df['Date'].values
    dfout = pd.DataFrame()
    dfout['time'] = time
    dfout['subject'] = subject
    dfout.to_csv('dat/subject_time.csv', index=False)

    


if __name__=='__main__':
    main()