import argparse

import pandas as pd

from utils import get_local_timestamp, merge_tables, convert_date


def parse_arguments():
    """
    Parses command-line arguments for the script.
    Arguments include paths to the test events table,video table, and the output file name.
    Returns an argparse Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Prepare one csv data with complex index.")

    parser.add_argument(
        '--test',
        type=str,
        help='Path to csv test events table.'
    )

    parser.add_argument(
        '--videos',
        default='video_info_v2.csv',
        help='Path to csv video table.'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='catboost_test.csv',
        help='Name of output csv test dataset file.'
    )
    return parser.parse_args()


def preprocess_table(test_path: str, video_path: str) -> pd.DataFrame:
    """
    Preprocesses the input CSV files for test predict.
    - Loads the test events and video tables from CSV files.
    - Merges the tables into one.
    - Applies timezone localization to the 'event_timestamp' field.
    - Adds 'value_counts' based on the 'viewer_uid'.
    - Converts the timestamp into date features using the convert_date function.

    Returns a preprocessed DataFrame.
    """
    test_df = pd.read_csv(test_path)
    video_info_df = pd.read_csv(video_path)

    merged_df = pd.merge(
        test_df,
        video_info_df,
        on='rutube_video_id',
        how='left'
    )
    print('Merged is done!')

    merged_df['event_timestamp'] = pd.to_datetime(merged_df['event_timestamp'])
    local_timestamp = get_local_timestamp(merged_df)

    merged_df['event_timestamp'] = local_timestamp.apply(lambda x: x.to_pydatetime())
    value_counts = merged_df.groupby('viewer_uid').apply(len).to_dict()
    merged_df['value_counts'] = merged_df['viewer_uid'].apply(lambda x: value_counts[x])
    df = convert_date(merged_df)
    return df


if __name__ == "__main__":
    args = parse_arguments()

    output_data = preprocess_table(
        test_path=args.test,
        video_path=args.videos
    )

    output_data.to_csv(args.output, index=False)
    print('Everything is done!')
