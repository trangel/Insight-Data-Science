def ModelIt(fromUser  = 'Default', births = []):
  import os
  print("path {}\n".format(os.getcwd()))
  in_month = len(births)
  print ('The number born is %i' % in_month)
  result = in_month
  if fromUser != 'Default':
    return result
  else:
    return 'check your input'
