import csv
import numpy as np
import pandas as pd
from argparse import ArgumentParser
#from clint.textui import colored

class SimpleQuery(object):

	def __init__(self):
		self.metricsNames = ['Id', 'AveCoefficient', 'AveFrequency', 'NumUsers', 'NumListens', 'AveListens']

def displayFacts(percentileDict, userInput):
	print(userInput + "...")
	for key in percentileDict:
		value = percentileDict[key]
		descriptor = ""
		extra_descriptor = ""
		if value == 99:
			descriptor += "n extremely high"
			extra_descriptor += "99th percentile"
		elif value == 95:
			descriptor += " very high"
			extra_descriptor += "95th percentile"
		elif value == 90:
			descriptor += " high"
			extra_descriptor += "90th percentile"
		elif value == 75:
			descriptor += " fairly high"
			extra_descriptor += "75th percentile"
		elif value == 50:
			descriptor += " average"
			extra_descriptor += "upper 50%"
		elif value == 25:
			descriptor += " fairly low"
			extra_descriptor += "bottom 50%"
		elif value == 0:
			descriptor += " very low"
			extra_descriptor += "bottom 25%"

		if key == 'AveCoefficient':
			print "\t + " + userInput + " has a" + descriptor + " coefficient of entropy; it falls in the " + extra_descriptor + ". This metric measures how diverse the music tastes of a fanbase are. Higher values mean fans typically listen to various musicians; low values mean they typically do not"
		elif key == 'AveFrequency':
			print ("\t + Listeners of " + userInput + " have a" + descriptor + " average listening frequency; it falls in the " + extra_descriptor + ". Listening frequency measures how many songs a fan listens to overall, from all artists combined. ")
		elif key == 'NumUsers':
			print ("\t + " + userInput + " has a" + descriptor + " number of unique listeners; it falls in the " + extra_descriptor + ". More unique listeners mean the artist has more brand recognition.")
		elif key == 'AveListens':
			print ("\t + Listeners of " + userInput + " listen to " + userInput + " at a" + descriptor + " rate; the number of average listens falls in the " + extra_descriptor + ". A higher number of listens per artist mean the fans are more dedicated to the artist.")


def getUserInputs(df, quantiles, querier):
	print('---------------------------')
	print('Input artist names below. Type \'q\' or \'Q\' to quit. ')
	while True:
		userInput = raw_input('> ')
		if userInput != 'q' and userInput != 'Q':
			percentileDict = {'AveCoefficient' : 0, 'AveFrequency' : 0, 'NumUsers' : 0, 'AveListens' : 0}
			columnsOfInterest = [1, 2, 3, 5]
			if not userInput in df.index:
				print("That artist does not exist. Please try again. ")
				continue

			row = df.loc[userInput]
			for x in range(len(quantiles.index)):
				copyColumns = list(columnsOfInterest)
				for y in range(len(columnsOfInterest)):
					if row.iloc[columnsOfInterest[y]] > quantiles.iloc[x, columnsOfInterest[y]]:
						percentile = int(float(quantiles.iloc[x].name) * 100)
						percentileDict[querier.metricsNames[columnsOfInterest[y]]] = percentile
						copyColumns[y] = -1

				columnsOfInterest = [x for x in copyColumns if x > -1]

			displayFacts(percentileDict, userInput)
			print('---------------------------')
		else:
			break


def main():
	querier = SimpleQuery()
	df = pd.read_csv('nowplaying-output-2.csv', sep = ',', index_col = 1)
	df[querier.metricsNames[5]] = df[querier.metricsNames[4]] / df[querier.metricsNames[3]]
	quantiles = df.quantile([.99, .95, .9, .75, .50, .25])
	getUserInputs(df, quantiles, querier)
	


if __name__=="__main__":
	main()	