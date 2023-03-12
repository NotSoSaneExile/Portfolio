def calculate_atr(df, period):
    df['high-low'] = df['High'] - df['Low']
    df['high-pc'] = abs(df['High'] - df['Close'].shift(1))
    df['low-pc'] = abs(df['Low'] - df['Close'].shift(1))
    df['true-range'] = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    atr = df['true-range'].rolling(period).mean()

    df.drop(['high-low', 'high-pc', 'low-pc', 'true-range'], axis=1, inplace=True)

    return atr