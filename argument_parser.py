

# This file contains the argument parser, that provides the basic functionality for the plotting tool.

class argument_parser():

	def read(self,arg):
		tel = {}
		if(type(arg) is str):
				arg = arg.split(" ")

		if type(arg) is dict:
			tel = arg
		else:
			for i in range(len(arg)):
				if arg[i][0]=='-':
					tel[arg[i][1:]] = "not set"
					if i+1 != len(arg):
						if arg[i+1][0]!='-':
							tel[arg[i][1:]] = arg[i+1]
							++i

			# convert everything that you can to numbers
		for i in tel:
			tel[i] = self.to_number(tel[i])

		return tel;

	def to_number(self,var):
		
			try:
				var = int(var)
			except:
				try:
					var = float(var)
				except:
					pass
				pass

			return var;

