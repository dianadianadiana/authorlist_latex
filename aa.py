import numpy as np
from astropy.table import Table
from astropy.io import ascii
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-file', default=None, required=True)
args = parser.parse_args()
fil = args.file

data = ascii.read(fil, format='csv',delimiter=',')

print('The column names: ')
print(data.colnames)
print()
print()

###################
### EMAIL LIST ####
###################

print('Email list:')
for email in data['Email']:
	if email != None:
		print(email, end=', ')
print()
print()
print()
###################
###################
###################

###################
### AUTHOR LIST ###
###################

print('Author list: ')
names = np.array([name for name in data['Author name']]) # 0.0 for names that are already there and have more than one affiliation
for ind, name in enumerate(names):
	if name == '0.0':
		names[ind] = names[ind-1]
unique_names = np.unique(names)
# unique_names is a list of unique names (not sorted by which was first)
# indexes is a list of indexes of where each name is found first (not sorted)
unique_names, indexes = np.unique(names, return_index=True)
# sort the indexes to create a sorted affiliation list
indexes_sorted = np.sort(indexes)
unique_names_sorted = []
for ind in indexes_sorted:
	ii = np.where(indexes==ind)[0]
	name = unique_names[ii][0]	
	unique_names_sorted = np.append(unique_names_sorted, name)
print('There are {} authors'.format(len(unique_names_sorted)))
for name in unique_names_sorted:
	print(name, end=', ')
print()
print()
print()
###################
###################
###################

###################
### SET UP OF #####
## NAMES AND ######
### AFFILITIONS ###
#### IN LATEX #####
###################

names_latex = np.array([name for name in data['Author name LaTeX']])
affiliations = np.array([name for name in data['Affiliation full address']])
affs_latex = np.array([name for name in data['Affiliation LaTeX']])
notes = np.array([name for name in data['Notes']])

# unique_affiliations is a list of unique affilitations (not sorted by which was first)
# indexes is a list of indexes of where each aff is found first (not sorted)
unique_affiliations, indexes = np.unique(affiliations, return_index=True)
print(unique_affiliations)
# sort the indexes to create a sorted affiliation list
indexes_sorted = np.sort(indexes)
unique_affiliations_sorted = []
for ind in indexes_sorted:
	ii = np.where(indexes==ind)[0]
	aff = unique_affiliations[ii][0]	
	unique_affiliations_sorted = np.append(unique_affiliations_sorted, aff)

print('The affiliations: ')
for aff in unique_affiliations_sorted:
	print(aff)
print()
print()

d = {}
for name in unique_names_sorted:
	inds = np.where(names==name)[0]
	latexname = names_latex[inds[0]]
	affs = affiliations[inds]
	aff_latex = affs_latex[inds]
	aff_nums = []
	for aff in affs:
		aff_nums = np.append(aff_nums, int(np.where(unique_affiliations_sorted==aff)[0]) +1)
	d[name] = [inds, latexname, aff_nums, aff, aff_latex, notes[inds][0]]


### For printing out the authors and affiliations
print()
print('Names and Affiliations (copy into overleaf)')
print()
print('\\author{')
for ii, k in enumerate(d.keys()):
	n = k if d[k][1]=='0.0' else d[k][1]
	if ii == 0:
		s = n+'\\inst{'
	else:
		s = '\\and '+ n+'\\inst{'
	for i in d[k][2]:
		s = s + str(int(i)) + ',' 
	s = s[:-1] # get rid of last comma
	s = s + '}'
	print(s)
print('}')

### For printing out the affiliations
print()
print('%Affiliation list (copy into overleaf)')
print()
print('\\institute{')
for ii, aff in enumerate(unique_affiliations_sorted):
	j = np.where(affiliations==aff)[0][0]
	aff_latex = affs_latex[j]
	a = aff if aff_latex == '0.0' else aff_latex
	if ii == 0:
		s = a + '\\\\' + ' %1' + '\n\\email{' + data['Email'][0] + '}'
	else:
		s = '\\and ' + a  + ' %' + str(int(ii+1)) #+ '\\\\'
	print(s)
print('}')

