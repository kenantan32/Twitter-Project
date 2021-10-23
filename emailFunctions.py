import pandas as pd
import frame

recipient = ''


def clear_data(x):  # to clear any data in the treeview
    x.delete(*x.get_children())
    return None


def readData(x, y, z):  # x = Treeview, y= by What column, z=Asc or Descending

    df = pd.read_csv(frame.file_path)  # reading and getting the dataframe
    df.sort_values(by=[y], inplace=True, ascending=z)  # sort function based on user inputs

    # This section populates the treeview frame that displays our data
    x["column"] = list(df.columns)
    x["show"] = "headings"
    for column in x["columns"]:
        x.heading(column, text=column)  # let the column heading = column name

    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        x.insert("", "end",
                 values=row)  # inserts each list into the treeview.
    return df.sort_values(by=[y], inplace=True, ascending=z)  # return the dataframe

def exportOnly(y, z):  # used to export ONLY
    df = pd.read_csv(frame.file_path)  # get dataframe (in this case file is selected by user)
    df.sort_values(by=[y], inplace=True, ascending=z)  # sorted according to user
    df.to_csv('DataSet.csv', index=False)  # saves the user's sort option and exports the file
