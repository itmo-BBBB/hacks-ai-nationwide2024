import argparse
import pandas as pd
import json

from utils import get_local_timestamp, merge_tables


def parse_arguments():
    """
    Parses command-line arguments required for processing CSV files.
    Returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Prepare csv data to the csv with json rows.")

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
        default='embedder_dataset.csv',
        help='Name of output csv dataset file.'
    )
    return parser.parse_args()


def preprocess_table(train_path: str, target_path: str, video_path: str) -> pd.Series:
    """
    Preprocesses the input CSV files by merging, grouping, and transforming data.
    Converts grouped data into a JSON string format suitable for model input.
    Returns a pandas Series of JSON-formatted records.
    """
    train_events_df = pd.read_csv(train_path)
    train_targets_df = pd.read_csv(target_path)
    video_info_df = pd.read_csv(video_path)

    merged_df = merge_tables(events=train_events_df, targets=train_targets_df, videos=video_info_df)
    merged_df['event_timestamp'] = pd.to_datetime(merged_df['event_timestamp'], errors='coerce')

    merged_df['event_timestamp'] = get_local_timestamp(merged_df).astype(str)

    user_columns = [
        'viewer_uid',
        'age',
        'age_class',
        'sex'
    ]
    video_columns = [
        'rutube_video_id',
        'title',
        'event_timestamp',
        'duration',
        'category',
        'author_id',
        'total_watchtime',
        'ua_device_type',
        'ua_client_type',
        'ua_client_name',
        'ua_os',
        'region'
    ]
    grouped_df = merged_df.groupby(user_columns).apply(
        lambda group: group[video_columns].to_dict(orient='records')
    ).reset_index()
    grouped_df = grouped_df.rename(columns={0: 'videos'})
    grouped_df['video_count'] = grouped_df['videos'].apply(len)

    json_list = grouped_df.to_dict(orient='records')
    result_series = pd.Series([json.dumps(record, ensure_ascii=False) for record in json_list]).astype(str)
    return result_series


if __name__ == "__main__":
    args = parse_arguments()

    output_data = preprocess_table(
        train_path=args.train,
        target_path=args.target,
        video_path=args.videos
    )

    output_data.to_csv(args.output, index=False)
    print('Everything is done!')
