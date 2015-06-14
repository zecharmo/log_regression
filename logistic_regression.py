import pandas as pd
import statsmodels.api as sm
import numpy as np

# retrieve data 
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# convert Interest Rate from a percent to a floating point number
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: round(float(x.rstrip('%')) / 100, 4))

# convert Loan Length to an integer
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: int(x.rstrip(' months')))

# convert FICO Range from a range to a single score
cleanFICORange = loansData['FICO.Range'].map(lambda x: x.split('-'))
cleanFICORange = cleanFICORange.map(lambda x: [int(n) for n in x])
cleanFICORange = cleanFICORange.map(lambda x: x.pop(0))
loansData['FICO.Score'] = cleanFICORange

# create a new column IR_TF that tells if the Interest Rate is > or < 12%
# if IR is > 12%, IR_TF will be 1, if IR is < 12%, IR_TF will be 0
loansData['IR_TF'] = loansData['Interest.Rate'].map(lambda x: 1 if x > .12 else 0)

# create a new column with a constant intercept of 1.0
loansData['Intercept'] = float(1.0)

# create a list of the column names
ind_vars = ['FICO.Score', 'Amount.Requested', 'Intercept']

# define the logistic regression model
logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

 
# fit the model
result = logit.fit()
 
# get the fitted coefficients from the results
coefficients = result.params
print coefficients
# Out: FICO.Score = -0.087423, Amount.Requested = 0.000174, Intercept = 60.125

# linear part of the predictor
#interest_rate = −60.125 + 0.087423(FicoScore) - 0.000174(LoanAmount)

# logistic function
def logistic_function(Intercept, Fico_Const, FicoScore, Loan_Const, LoanAmount):
	p = 1/(1 + e^(Intercept + Fico_Const * (FicoScore) - Loan_Const * (LoanAmount)))
	return 
print p

# test condition, probability of getting a $10000 loan with a credit score of 720
logistic_function(coefficient['Intercept'], coefficent['FICO.Score'], 720, coefficient['Amount.Requested'], 10000)
# Out: 0.74637

# Probability of getting a $10000 loan with a credit score of 720 is 74.6%