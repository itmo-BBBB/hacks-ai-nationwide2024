import pandas as pd
import numpy as np
import pytz

from typing import Tuple


def merge_tables(events: pd.DataFrame, targets: pd.DataFrame, videos: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the events, targets, and videos DataFrames based on shared columns.
    First, merges events with targets using 'viewer_uid', then merges the result with videos on 'rutube_video_id'.
    Returns the merged DataFrame.
    """
    premerged_df = pd.merge(
        events,
        targets,
        on='viewer_uid',
        how='outer'
    )

    merged_df = pd.merge(
        premerged_df,
        videos,
        on='rutube_video_id',
        how='left'
    )
    print('Merged is done!')
    return merged_df


def get_local_timestamp(df: pd.DataFrame) -> pd.Series:
    """
    Localizes the 'event_timestamp' column of the DataFrame based on the 'region' column.
    Adjusts the timestamp to the correct local time zone according to the specified region.
    Returns a pandas Series of localized timestamps.
    """

    region_to_timezone = {
        'Moscow': 'Europe/Moscow',
        'Moscow Oblast': 'Europe/Moscow',
        'St.-Petersburg': 'Europe/Moscow',
        "Leningradskaya Oblast'": 'Europe/Moscow',
        'Adygeya Republic': 'Europe/Moscow',
        'Altai': 'Asia/Barnaul',
        'Altay Kray': 'Asia/Barnaul',
        'Amur Oblast': 'Asia/Yakutsk',
        'Arkhangelsk Oblast': 'Europe/Moscow',
        'Arkhangelskaya': 'Europe/Moscow',
        'Astrakhan': 'Europe/Samara',
        'Astrakhan Oblast': 'Europe/Samara',
        'Bashkortostan Republic': 'Asia/Yekaterinburg',
        'Belgorod Oblast': 'Europe/Moscow',
        'Bryansk Oblast': 'Europe/Moscow',
        'Buryatiya Republic': 'Asia/Irkutsk',
        'Chechnya': 'Europe/Moscow',
        'Chelyabinsk': 'Asia/Yekaterinburg',
        'Chukotka': 'Asia/Anadyr',
        'Chuvashia': 'Europe/Moscow',
        'Crimea': 'Europe/Simferopol',
        'Dagestan': 'Europe/Moscow',
        'Ingushetiya Republic': 'Europe/Moscow',
        'Irkutsk Oblast': 'Asia/Irkutsk',
        'Ivanovo': 'Europe/Moscow',
        'Ivanovo Oblast': 'Europe/Moscow',
        'Jaroslavl': 'Europe/Moscow',
        'Jewish Autonomous Oblast': 'Asia/Vladivostok',
        'Kabardino-Balkariya Republic': 'Europe/Moscow',
        'Kaliningrad': 'Europe/Kaliningrad',
        'Kaliningrad Oblast': 'Europe/Kaliningrad',
        'Kalmykiya Republic': 'Europe/Moscow',
        'Kaluga': 'Europe/Moscow',
        'Kaluga Oblast': 'Europe/Moscow',
        'Kamchatka': 'Asia/Kamchatka',
        'Karachayevo-Cherkesiya Republic': 'Europe/Moscow',
        'Karelia': 'Europe/Moscow',
        'Kemerovo Oblast': 'Asia/Novokuznetsk',
        'Khabarovsk': 'Asia/Vladivostok',
        'Khakasiya Republic': 'Asia/Krasnoyarsk',
        'Khanty-Mansia': 'Asia/Yekaterinburg',
        'Kirov': 'Europe/Moscow',
        'Kirov Oblast': 'Europe/Moscow',
        'Komi': 'Europe/Moscow',
        'Kostroma Oblast': 'Europe/Moscow',
        'Krasnodar Krai': 'Europe/Moscow',
        'Krasnodarskiy': 'Europe/Moscow',
        'Krasnoyarsk Krai': 'Asia/Krasnoyarsk',
        'Krasnoyarskiy': 'Asia/Krasnoyarsk',
        'Kurgan Oblast': 'Asia/Yekaterinburg',
        'Kursk': 'Europe/Moscow',
        'Kursk Oblast': 'Europe/Moscow',
        'Kuzbass': 'Asia/Novokuznetsk',
        'Lipetsk Oblast': 'Europe/Moscow',
        'Magadan Oblast': 'Asia/Magadan',
        'Mariy-El Republic': 'Europe/Moscow',
        'Mordoviya Republic': 'Europe/Moscow',
        'Murmansk': 'Europe/Moscow',
        'Nenets': 'Europe/Moscow',
        'Nizhny Novgorod Oblast': 'Europe/Moscow',
        'North Ossetia': 'Europe/Moscow',
        'North Ossetia–Alania': 'Europe/Moscow',
        'Novgorod Oblast': 'Europe/Moscow',
        'Novosibirsk Oblast': 'Asia/Novosibirsk',
        'Omsk': 'Asia/Omsk',
        'Omsk Oblast': 'Asia/Omsk',
        'Orel Oblast': 'Europe/Moscow',
        'Orenburg Oblast': 'Asia/Yekaterinburg',
        'Oryol oblast': 'Europe/Moscow',
        'Penza': 'Europe/Samara',
        'Penza Oblast': 'Europe/Samara',
        'Perm': 'Asia/Yekaterinburg',
        'Perm Krai': 'Asia/Yekaterinburg',
        'Primorskiy (Maritime) Kray': 'Asia/Vladivostok',
        'Primorye': 'Asia/Vladivostok',
        'Pskov Oblast': 'Europe/Moscow',
        'Rostov': 'Europe/Moscow',
        'Ryazan Oblast': 'Europe/Moscow',
        'Sakha': 'Asia/Yakutsk',
        'Sakhalin Oblast': 'Asia/Sakhalin',
        'Samara Oblast': 'Europe/Samara',
        'Saratov Oblast': 'Europe/Saratov',
        'Saratovskaya Oblast': 'Europe/Saratov',
        'Sebastopol City': 'Europe/Simferopol',
        'Smolensk': 'Europe/Moscow',
        'Smolensk Oblast': 'Europe/Moscow',
        'Smolenskaya Oblast’': 'Europe/Moscow',
        'Stavropol Krai': 'Europe/Moscow',
        'Stavropol Kray': 'Europe/Moscow',
        'Stavropol’ Kray': 'Europe/Moscow',
        'Sverdlovsk': 'Asia/Yekaterinburg',
        'Sverdlovsk Oblast': 'Asia/Yekaterinburg',
        'Tambov': 'Europe/Moscow',
        'Tambov Oblast': 'Europe/Moscow',
        'Tatarstan Republic': 'Europe/Moscow',
        'Tomsk Oblast': 'Asia/Tomsk',
        'Transbaikal Territory': 'Asia/Chita',
        'Tula': 'Europe/Moscow',
        'Tula Oblast': 'Europe/Moscow',
        'Tver Oblast': 'Europe/Moscow',
        'Tver’ Oblast': 'Europe/Moscow',
        'Tyumen Oblast': 'Asia/Yekaterinburg',
        'Tyumen’ Oblast': 'Asia/Yekaterinburg',
        'Tyva Republic': 'Asia/Krasnoyarsk',
        'Udmurtiya Republic': 'Europe/Samara',
        'Ulyanovsk': 'Europe/Samara',
        'Vladimir': 'Europe/Moscow',
        'Vladimir Oblast': 'Europe/Moscow',
        'Volgograd Oblast': 'Europe/Volgograd',
        'Vologda': 'Europe/Moscow',
        'Vologda Oblast': 'Europe/Moscow',
        'Voronezh Oblast': 'Europe/Moscow',
        'Voronezj': 'Europe/Moscow',
        'Yamalo-Nenets': 'Asia/Yekaterinburg',
        'Yaroslavl Oblast': 'Europe/Moscow',
        'Zabaykalskiy (Transbaikal) Kray': 'Asia/Chita'
    }

    timezonecolumn = df['region'].map(region_to_timezone)

    def localize_timestamp(row):
        if not isinstance(row['event_timestamp'], pd.Timestamp):
            row['event_timestamp'] = pd.to_datetime(row['event_timestamp'])

        if row['event_timestamp'].tzinfo is not None:
            row['event_timestamp'] = row['event_timestamp'].tz_localize(None)

        timezone = timezonecolumn[row.name]
        new_tz = pytz.timezone(timezone)
        old_tz = pytz.timezone('Europe/Moscow')

        localized_timestamp = old_tz.localize(row['event_timestamp']).astimezone(new_tz)
        return localized_timestamp

    print('Local date is done!')
    return df.apply(localize_timestamp, axis=1)


def convert_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts date-related features (year, month, day, hour, etc.) from the 'event_timestamp' column.
    Additionally, adds cyclical hour features (sin and cos transformations) for better model processing.
    Returns the modified DataFrame with new date-related columns and drops the 'event_timestamp' column.
    """
    date_feature = "event_timestamp"

    df['year'] = df[date_feature].apply(lambda x: x.year)
    df['month'] = df[date_feature].apply(lambda x: x.month)
    df['day'] = df[date_feature].apply(lambda x: x.day)
    df['hour'] = df[date_feature].apply(lambda x: x.hour)
    df['minute'] = df[date_feature].apply(lambda x: x.minute)
    df['second'] = df[date_feature].apply(lambda x: x.second)
    df['day_of_week'] = df[date_feature].apply(lambda x: x.weekday())

    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

    print('Convert date is done!')
    return df.drop(date_feature, axis=1)

