import pandas as pd

def simple_moving_average(prices: pd.Series, n: int) -> pd.Series:
  """
  Calculate simple n-day moving average for given data.
  
  Params:
    prices:
    n:
  """
  return prices.rolling(window=n).mean()


def weighted_moving_average(prices: pd.Series, n: int) -> pd.Series:
  """
  Calculate weighted n-day moving average for given data.

  Params:
      
  Returns:
  """
  return prices.rolling(window=n).apply(lambda x: x[::-1].cumsum().sum() * 2 / n / (n + 1))


def exponential_moving_average(prices: pd.Series, n: int) -> pd.Series:
    """
    Calculate exponential n-day moving average for given data.

    Params:
        
    Returns:
    """
    return prices.ewm(span=n).mean()
  
  
def relative_strength_index(prices: pd.Series, n: int) -> pd.Series:
  """
  Calculate n-day relative strength index for given data.

  Params:

  Returns:
  """
  deltas = prices.diff()
  ups = deltas.clip(lower=0)
  downs = (-deltas).clip(lower=0)
  rs = ups.ewm(com=n-1, min_periods=n).mean() / downs.ewm(com=n-1, min_periods=n).mean()

  return 100 - 100 / (1 + rs)


def stochastic_oscillator(d_type='sma': str, prices: pd.Series, n: int) -> pd.Series:
  """
  Calculate n-day stochastic %K and %D for given data.

  Params:

  Returns:
  """
  highest_high = prices.rolling(window=n).max()
  lowest_low = prices.rolling(window=n).min()

  stochastic_k = ((prices - lowest_low) / (highest_high - lowest_low)) * 100

  if d_type == 'sma': 
      stochastic_d = simple_moving_average(stochastic_k, n)
  elif d_type == 'wma':
      stochastic_d = weighted_moving_average(stochastic_k, n)
  elif d_type == 'ema':
      stochastic_d = exponential_moving_average(stochastic_k, n)
  else:
      raise ValueError('Only sma, wma and ema are available.')

  return stochastic_k, stochastic_d
 