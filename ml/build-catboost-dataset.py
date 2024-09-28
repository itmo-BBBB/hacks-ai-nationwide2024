import argparse

import pandas as pd

from utils import get_local_timestamp, merge_tables, convert_date


def parse_arguments():
    """
    Parses command-line arguments for the script.
    Arguments include paths to the train events table, target table, video table, and the output file name.
    Returns an argparse Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Prepare one csv data with complex index.")

    parser.add_argument(
        '--train',
        type=str,
        help='Path to csv train events table.'
    )

    parser.add_argument(
        '--target',
        type=str,
        help='Path to csv target table.'
    )

    parser.add_argument(
        '--videos',
        default='video_info_v2.csv',
        help='Path to csv video table.'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='catboost_dataset.csv',
        help='Name of output csv dataset file.'
    )
    return parser.parse_args()


def preprocess_table(train_path: str, target_path: str, video_path: str) -> pd.DataFrame:
    """
    Preprocesses the input CSV files for training.
    - Loads the train events, target, and video tables from CSV files.
    - Merges the tables into one.
    - Applies timezone localization to the 'event_timestamp' field.
    - Adds 'value_counts' based on the 'viewer_uid'.
    - Converts the timestamp into date features using the convert_date function.

    Returns a preprocessed DataFrame.
    """
    train_events_df = pd.read_csv(train_path)
    train_targets_df = pd.read_csv(target_path)
    video_info_df = pd.read_csv(video_path)

    merged_df = merge_tables(events=train_events_df, targets=train_targets_df, videos=video_info_df)
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
        train_path=args.train,
        target_path=args.target,
        video_path=args.videos
    )

    output_data.to_csv(args.output, index=False)
    print('Everything is done!')
