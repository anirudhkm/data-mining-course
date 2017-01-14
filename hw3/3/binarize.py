import pandas as pd

def binarize_data(file_name):
    """
    This function helps to binarize
    the input data and stores them in a file
    """

    df = pd.read_csv(file_name)
    # load data in a dataframe
    for col in df.columns:
        # iterate over each column
        data = df[col].unique()
        ratio = round(0.5*len(data))
        for i in data[:ratio]:
            df[col][df[col] == i] = 1
        for i in data[ratio:]:
            df[col][df[col] == i] = 0
    df.to_csv("binary_"+file_name, index = False)
    return df

bdf = binarize_data("nursery.data")
