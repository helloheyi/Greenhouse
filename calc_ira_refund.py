import pandas as pd
import numpy as np


MAX_IRA_CONTRIB_UNDER_50 = 5500
MAX_IRA_CONTRIB_50_AND_ABOVE = 6500
CONTRIBUTION_CUTOFF_AGE = 71
PERSONAL_EXEMPTION = 4050


class FilingStatus:
    SINGLE = 0
    MARRIED_JOINTLY = 1
    MARRIED_SEPARATELY = 2
    HEAD_OF_HOUSEHOLD = 3
    

standard_deductions = pd.Series(data=[(FilingStatus.SINGLE, 6300),
                                      (FilingStatus.MARRIED_JOINTLY, 12600),
                                      (FilingStatus.MARRIED_SEPARATELY, 6300),
                                      (FilingStatus.HEAD_OF_HOUSEHOLD, 9300)])



#marginal tax rates
single_tax_rates = pd.DataFrame(columns=['income_lb','income_ub','marginal_rate'])
single_tax_rates.loc[0] = [0, 9275, 0.10]
single_tax_rates.loc[1] = [9276, 37650, 0.15]
single_tax_rates.loc[2] = [37651, 91150, 0.25]
single_tax_rates.loc[3] = [91151, 190150, 0.28]
single_tax_rates.loc[4] = [190151, 413350, 0.33]
single_tax_rates.loc[5] = [413351, 415050, 0.35]
single_tax_rates.loc[6] = [415051, np.inf, 0.396]


married_jointly_tax_rates = pd.DataFrame(columns=['income_lb','income_ub','marginal_rate'])
married_jointly_tax_rates.loc[0] = [0, 18550, 0.10]
married_jointly_tax_rates.loc[1] = [18551, 75300, 0.15]
married_jointly_tax_rates.loc[2] = [75301, 151900, 0.25]
married_jointly_tax_rates.loc[3] = [151901, 231450, 0.28]
married_jointly_tax_rates.loc[4] = [231451, 413350, 0.33]
married_jointly_tax_rates.loc[5] = [413351, 466950, 0.35]
married_jointly_tax_rates.loc[6] = [466951, np.inf, 0.396]


married_separately_tax_rates = pd.DataFrame(columns=['income_lb','income_ub','marginal_rate'])
married_separately_tax_rates.loc[0] = [0, 9275, 0.10]
married_separately_tax_rates.loc[1] = [9276, 37650, 0.15]
married_separately_tax_rates.loc[2] = [37651, 75950, 0.25]
married_separately_tax_rates.loc[3] = [75951, 115725, 0.28]
married_separately_tax_rates.loc[4] = [115726, 206675, 0.33]
married_separately_tax_rates.loc[5] = [206676, 233475, 0.35]
married_separately_tax_rates.loc[6] = [233476, np.inf, 0.396]


head_of_household_tax_rates = pd.DataFrame(columns=['income_lb','income_ub','marginal_rate'])
head_of_household_tax_rates.loc[0] = [0, 13250, 0.10]
head_of_household_tax_rates.loc[1] = [13251, 50400, 0.15]
head_of_household_tax_rates.loc[2] = [50401, 130150, 0.25]
head_of_household_tax_rates.loc[3] = [130151, 210800, 0.28]
head_of_household_tax_rates.loc[4] = [210801, 413350, 0.33]
head_of_household_tax_rates.loc[5] = [413351, 441000, 0.35]
head_of_household_tax_rates.loc[6] = [441001, np.inf, 0.396]


#need to account for the case where the tax deduction causes you to drop to a lower marginal tax rate


def compute_tax_payable(income, filing_status):
    if filing_status==FilingStatus.SINGLE:
        lookup_table = single_tax_rates
    elif filing_status==FilingStatus.MARRIED_SEPARATELY:
        lookup_table = married_separately_tax_rates
    elif filing_status==FilingStatus.MARRIED_JOINTLY:
        lookup_table = married_jointly_tax_rates
    elif filing_status==FilingStatus.HEAD_OF_HOUSEHOLD:
        lookup_table = head_of_household_tax_rates
    else:
        raise Exception("Invalid choice")
    
    taxes = 0
    
    for i in range(len(lookup_table)):
            if (income >= lookup_table.loc[i,'income_lb']):
                taxes += lookup_table.loc[i,'marginal_rate'] * (np.min([income, lookup_table.loc[i, 'income_ub']]) - lookup_table.loc[i, 'income_lb'])
                
    return taxes


def compute_allowable_pct(lb, ub, income):
    if (income < lb) | (income > ub):
        raise Exception("Income not within bounds")
    
    return 1.0 - ( (income - lb) / (ub - lb) )
    

def compute_tax_refund(contribution, has_retirement_plan_at_work, spouse_has_retirement_plan_at_work, income, filing_status, age):
    
    #cap the contribution based on age
    if age < 50:
        contribution = np.min([contribution, MAX_IRA_CONTRIB_UNDER_50, income])
    else:
        contribution = np.min([contribution, MAX_IRA_CONTRIB_50_AND_ABOVE, income])
    
    #use adjusted income    
    income = income - contribution
    
    if age >= CONTRIBUTION_CUTOFF_AGE:
        return 0 #no contributions allowed
    
    if has_retirement_plan_at_work:
        if filing_status==FilingStatus.SINGLE:
            if income <= 61000:
                #full deduction
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-contribution, filing_status)
            elif (income >= 61000) & (income < 71000):
                #partial deduction
                allowed_contrib = compute_allowable_pct(61000,71000,income) * contribution
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-allowed_contrib, filing_status)
            elif income >= 71000:
                return 0
        elif filing_status==FilingStatus.HEAD_OF_HOUSEHOLD:
            if income <= 61000:
                #full deduction
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-contribution, filing_status)
            elif (income >= 61000) & (income < 71000):
                #partial deduction
                allowed_contrib = compute_allowable_pct(61000,71000,income) * contribution
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-allowed_contrib, filing_status)                
            elif income >= 71000:
                return 0            
        elif filing_status==FilingStatus.MARRIED_JOINTLY:
            if income <= 98000:
                #full deduction
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-contribution, filing_status)
            elif (income > 98000) & (income < 118000):
                #partial deduction
                allowed_contrib = compute_allowable_pct(98000,118000,income) * contribution
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-allowed_contrib, filing_status)
            elif income >= 118000:
                return 0
        elif filing_status==FilingStatus.MARRIED_SEPARATELY:
            if income < 10000:
                #partial deduction
                allowed_contrib = compute_allowable_pct(0,10000,income) * contribution
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-allowed_contrib, filing_status)                
            else:
                return 0
    else: #No retirement plan at work
        if (filing_status==FilingStatus.SINGLE) | (filing_status==FilingStatus.HEAD_OF_HOUSEHOLD):
            #full deduction up to contrib limit, any income
            return compute_tax_payable(income, filing_status) - compute_tax_payable(income-contribution, filing_status)
            
        elif ((filing_status==FilingStatus.MARRIED_SEPARATELY) | (filing_status==FilingStatus.MARRIED_JOINTLY)) & (~spouse_has_retirement_plan_at_work):
            #full deduction up to contrib limit, any income        
            return compute_tax_payable(income, filing_status) - compute_tax_payable(income-contribution, filing_status)
        
        elif (filing_status==FilingStatus.MARRIED_JOINTLY) & (spouse_has_retirement_plan_at_work):
           
            if income <= 184000:
                #full deduction up to contrib limit                
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-contribution, filing_status)
            elif (income > 184000) & (income < 194000):
                #partial deduction
                allowed_contrib = compute_allowable_pct(184000,194000,income) * contribution
                return compute_tax_payable(income, filing_status) - compute_tax_payable(income-allowed_contrib, filing_status)                
            elif income >= 194000:
                return 0 #no deduction allowed
            elif (filing_status==FilingStatus.MARRIED_SEPARATELY) & spouse_has_retirement_plan_at_work:
                if income < 10000:
                    #partial deduction
                    allowed_contrib = compute_allowable_pct(0,10000,income) * contribution
                    return compute_tax_payable(income, filing_status) - compute_tax_payable(income-allowed_contrib, filing_status)                    
                else:
                    return 0 #no deduction allowed



if __name__=="__main__":
    
    #params
    has_retirement_plan_at_work = False
    spouse_has_retirement_plan_at_work = False
    contribution = 3e3
    modified_agi = 70e3 #modified adjusted gross income
    filing_status = FilingStatus.SINGLE
    age = 30
    
    #compute refund
    refund = compute_tax_refund(contribution, has_retirement_plan_at_work, spouse_has_retirement_plan_at_work, modified_agi, filing_status, age)
    print "Refund: {}".format(refund)
    
    
