import pandas as pd
from glob import glob
from datetime import timedelta
import pytz # タイムゾーン処理のため

# --- 設定項目 ---
ZIGZAG_DATA_PATH = "csv/Zigzag-data/mt5_zigzag_legs_*.csv"
OUTPUT_CSV_PATH = "csv/CalculatedVolatility/intraday_volatility.csv"

# JST時間帯の定義 (開始時, 終了時)
# 例: 7時00分から8時59分まで (9時は含まない)
JST_TIME_RANGES = [
    (7, 9),
    (9, 12),
    (12, 15),
    (15, 21),
    (21, 24), # 21:00 JST to 23:59 JST (exclusive of 24:00)
    (0, 3),   # 00:00 JST to 02:59 JST (exclusive of 03:00)
    (3, 7)    # 03:00 JST to 06:59 JST (exclusive of 07:00)
]

# --- ヘルパー関数 ---
def convert_to_jst(dt_series_utc_naive):
    """
    pandas Series の naive datetime オブジェクト (UTCと仮定) をJSTに変換する。
    """
    return dt_series_utc_naive.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')


# --- メイン処理 ---
def main():
    all_files = glob(ZIGZAG_DATA_PATH)
    if not all_files:
        print(f"No files found at {ZIGZAG_DATA_PATH}")
        return

    df_list = []
    for f in all_files:
        try:
            df_temp = pd.read_csv(f, sep='\t')
            required_cols = ['start_time_utc_seconds', 'end_time_utc_seconds', 'start_price', 'end_price']
            if not all(col in df_temp.columns for col in required_cols):
                print(f"Skipping file {f} due to missing one or more required columns: {', '.join(required_cols)}.")
                continue
            df_list.append(df_temp)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue
    
    if not df_list:
        print("No valid ZigZag data could be loaded.")
        return

    df_zigzag = pd.concat(df_list, ignore_index=True)

    try:
        df_zigzag['start_time_dt'] = pd.to_datetime(df_zigzag['start_time_utc_seconds'], unit='s')
        df_zigzag['end_time_dt'] = pd.to_datetime(df_zigzag['end_time_utc_seconds'], unit='s')
    except KeyError as e:
        print(f"KeyError: One of the critical time columns ('start_time_utc_seconds' or 'end_time_utc_seconds') is missing. Error: {e}")
        return
    except ValueError as e:
        print(f"ValueError: Could not convert time columns to datetime. Ensure they are Unix timestamps in seconds. Error: {e}")
        return
    except Exception as e: # Other potential errors during conversion
        print(f"An unexpected error occurred during time column conversion: {e}")
        return

    df_zigzag['start_time_jst'] = convert_to_jst(df_zigzag['start_time_dt'])
    df_zigzag['end_time_jst'] = convert_to_jst(df_zigzag['end_time_dt'])

    results = []

    unique_dates_jst = df_zigzag['start_time_jst'].dt.normalize().unique()

    for current_date_jst_norm in unique_dates_jst: 
        for start_hour_jst, end_hour_jst in JST_TIME_RANGES:
            
            start_datetime_jst_tz = current_date_jst_norm.replace(hour=start_hour_jst, minute=0, second=0, microsecond=0)
            
            if end_hour_jst == 24:
                end_datetime_jst_tz = (current_date_jst_norm + pd.Timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                end_datetime_jst_tz = current_date_jst_norm.replace(hour=end_hour_jst, minute=0, second=0, microsecond=0)
            
            mask = (
                (df_zigzag['start_time_jst'] >= start_datetime_jst_tz) &
                (df_zigzag['start_time_jst'] < end_datetime_jst_tz)
            )
            
            legs_in_range = df_zigzag[mask]

            if not legs_in_range.empty:
                prices_in_legs = pd.concat([legs_in_range['start_price'], legs_in_range['end_price']]).dropna()
                
                if not prices_in_legs.empty:
                    max_high_in_range = prices_in_legs.max()
                    min_low_in_range = prices_in_legs.min()
                    price_movement = max_high_in_range - min_low_in_range
                else:
                    max_high_in_range = None
                    min_low_in_range = None
                    price_movement = 0
                
                results.append({
                    "Date_JST": current_date_jst_norm.strftime('%Y-%m-%d'),
                    "TimeRange_JST": f"{str(start_hour_jst).zfill(2)}:00-{str(end_hour_jst).zfill(2)}:00",
                    "PriceMovement": price_movement,
                    "MaxHigh_in_Range": max_high_in_range,
                    "MinLow_in_Range": min_low_in_range
                })
            else:
                results.append({
                    "Date_JST": current_date_jst_norm.strftime('%Y-%m-%d'),
                    "TimeRange_JST": f"{str(start_hour_jst).zfill(2)}:00-{str(end_hour_jst).zfill(2)}:00",
                    "PriceMovement": 0, 
                    "MaxHigh_in_Range": None,
                    "MinLow_in_Range": None
                })

    df_results = pd.DataFrame(results)
    
    output_dir = "/".join(OUTPUT_CSV_PATH.split("/")[:-1])
    if output_dir:
        import os
        if not os.path.exists(output_dir):
             os.makedirs(output_dir, exist_ok=True)

    df_results.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Volatility data saved to {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main() 