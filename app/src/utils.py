def convert_hex_to_rgb(hex_string):
  """
  Returns: [hex_string] converted to a rgb tuple.
  """
  h = hex_string.lstrip('#')
  return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
