import sys
import pandas as pd

if __name__ == '__main__':
    data_file = sys.argv[1]
    corr_method = sys.argv[2]
    output_file = sys.argv[3]
    df = pd.read_csv(data_file)
    result = df.corr(method=corr_method)
    result.to_csv(output_file, header=True, index=True)
