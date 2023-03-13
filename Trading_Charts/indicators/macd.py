def calculate_macd(df, n_fast, n_slow, n_signal):
    ema_fast = df['Close'].ewm(span=n_fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=n_slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=n_signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram