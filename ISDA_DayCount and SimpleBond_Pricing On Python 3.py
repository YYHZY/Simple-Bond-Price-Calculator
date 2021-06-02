#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
##dayCount 1 thirty_360Isda
##dayCount 2 thirty_360
##dayCount 3 thirty_360E
##dayCount 4 act360
##dayCount 5 act365
##dayCount 6 actAct


# In[2]:


def isLeapYear(d):
    if (( d.year%400 == 0)or (( d.year%4 == 0 ) and ( d.year%100 != 0))):
        return "true"

class act365:
    def yearFraction(d0, d1):
        return (d1 - d0).days / 365
    def daysInbetween(d0,d1):
        return (d1 - d0).days 
    
class act360:
    def yearFraction(d0, d1): 
        return (d1 - d0).days / 360
    def daysInbetween(d0,d1):
        return (d1 - d0).days

class actAct:
    def yearFraction(c0,c1,d0):
        couponDays = (c1-c0).days
        actualDays = (d0-c0).days
        return actualDays / couponDays
    def daysInbetween(d0,c0):
        return (d0 - c0).days 
    
class thirty_360E:
    def daysInbetween(d0,d1):
        years = d1.year-d0.year
        months = d1.month - d0.month
        if d0.day == 31:
            day0 = 30
        else:
            day0 = d0.day
            
        if d1.day ==31:
            day1 = 30    
        else:
            day1 =d1.day 
        totalDays = years*360 + months*30 + day1 - day0
        return totalDays
    def yearFraction (d0,d1):
        return thirty_360E.daysInbetween(d0,d1)/360 

class thirty_360:
    def daysInbetween(d0,d1):
        years = d1.year-d0.year
        months = d1.month - d0.month
        if d0.day == 31:
            day0 = 30
        else:
            day0 = d0.day

        if d1.day==30 or d1.day==31:
            day1 = min (d1.day,31)   
        else:
            day1 =d1.day          
        totalDays = years*360 + months*30 + day1 - day0
        return totalDays
    def yearFraction (d0,d1):
        return thirty_360.daysInbetween(d0,d1)/360 


class thirty_360Isda:
    def daysInbetween(d0,d1):
        years = d1.year-d0.year
        months = d1.month - d0.month
        if isLeapYear(d0)=="true":
            if d0.month==2 and d0.day==29:
                day0 = 30
            else:
                day0 = d0.day
            
        elif (d0.month==2 and d0.day==28) or d0.day==31:
            day0 = 30
        else:
            day0 = d0.day
            
        if isLeapYear(d1)=="true":
            if d1.month==2 and d1.day==29:
                day1 = 30
            else:
                day1 = d1.day
        elif (d1.month==2 and d1.day==28) or d1.day ==31:
            day1 = 30
        else:
            day1 = d1.day
        
        totalDays = years*360 + months*30 + day1 - day0
        return totalDays
    def yearFraction (d0,d1):
        return thirty_360Isda.daysInbetween(d0,d1)/360 


# In[3]:


import math

def discFactor(d0,d1,dayCount,YTM,freq,anni):
    if dayCount == 1:
        return math.exp(-YTM * thirty_360Isda.yearFraction(d0,d1))
    if dayCount == 2:
        return math.exp(-YTM * thirty_360.yearFraction(d0,d1))
    if dayCount == 3:
        return math.exp(-YTM * thirty_360E.yearFraction(d0,d1))
    if dayCount == 4:
        return math.exp(-YTM * act360.yearFraction(d0,d1))
    if dayCount == 5:
        return math.exp(-YTM * act365.yearFraction(d0,d1))


# In[4]:


##Buidling up the interest schedule

import datetime
from dateutil.relativedelta import relativedelta
class intScheduel:
    def nextCouponDate(valueDate,maturityDate,freq,anni):
        ###YANG WOZ HERE
        x=date(valueDate.year,anni.month,anni.day)
        for i in range (freq):
            #print("count",i)
            y = x + relativedelta(months=+int(12/freq)*i)
            if valueDate <= y:
                break                         
        nextCouponDate = y
        return nextCouponDate
    
    #Based on the next coupon date, we can look back and find the previous coupon
    def preCouponDate(nextCouponDate,freq):      
        preCouponDate = nextCouponDate - relativedelta(months=+int(12/freq))  
        return preCouponDate
    
    def firstCouponDate(valueDate,issueDate,maturityDate,freq,anni,firstStub):
        firstCouponDate = intScheduel.nextCouponDate(issueDate,maturityDate,freq,anni)
        if firstStub =="long":   
            firstCouponDate = firstCouponDate + relativedelta(months=+int(12/freq))
        return firstCouponDate
    
    def isFirstPeriod(valueDate,issueDate,maturityDate,freq,anni,firstStub):
        firstCouponDate = firstCouponDate (valueDate,issueDate,maturityDate,freq,anni,firstStub)
        if valueDate > issueDate and valueDate < firstCouponDate:
            return "true"
        else:
            return "false"
    
    def secondFinalCouponDate(valueDate,issueDate,maturityDate,freq,anni,finalStub):
        nextCouponDate = intScheduel.nextCouponDate(maturityDate,maturityDate,freq,anni)
        #print("hypoNextCoup",nextCouponDate)
        #The coupon date before maturity
        secondFinalCouponDate = nextCouponDate - relativedelta(months=+int(12/freq))
        if finalStub =="long":
            secondFinalCouponDate = secondFinalCouponDate - relativedelta(months=+int(12/freq))  
        #print("secondfinalCouponDate",secondfinalCouponDate)
        return secondFinalCouponDate
    
    def isFinalPeriod(valueDate,issueDate,maturityDate,freq,anni,finalStub):
        nextCouponDate = intScheduel.nextCouponDate(maturityDate,maturityDate,freq,anni)
        #The coupon date before maturity
        secondFinalCouponDate = intScheduel.preCouponDate(nextCouponDate,freq)
        finalCouponDate = maturityDate
        if finalStub =="long":
            secondFinalCouponDate = secondFinalCouponDate  - relativedelta(months=+int(12/freq))    
        if finalCouponDate > valueDate and valueDate > secondFinalCouponDate:
            return "true"
        else:
            return "false"

    def finalInterest(valueDate,issueDate,maturityDate,dayCount,rate,freq,anni,finalStub):
        #The coupon date before maturity
        secondfinalCouponDate = intScheduel.secondFinalCouponDate(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        finalCouponDate = maturityDate
        if finalStub == "false":
            finalInterest = 100*rate/freq
        else:    
            finalInterest = 100*rate*yearFraction(secondfinalCouponDate,finalCouponDate,dayCount,freq,anni)
        return finalInterest
    
    
    def firstInterest(valueDate,issueDate,maturityDate,dayCount,rate,freq,anni,finalStub):
        firstCouponDate = intScheduel.nextCouponDate(issueDate,maturityDate,freq,anni)
        if firstStub =="long":   
            firstCouponDate = firstCouponDate + relativedelta(months=+int(12/freq))
        if firstStub == "false":
            firstInterest = 100*rate/freq
        else:    
            firstInterest = 100*rate*yearFraction(issueDate,firstCouponDate,dayCount,freq,anni)
        return firstInterest
        
    def couponPeriods(valueDate,maturityDate,freq,anni,firstStub, finalStub):
        nextCouponDate = intScheduel.nextCouponDate(valueDate,maturityDate,freq,anni)
        months = (maturityDate.year-nextCouponDate.year) *12 + (maturityDate.month-nextCouponDate.month)
        couponPeriods = math.ceil(months / (12/freq))+1
        if finalStub == "short":
            couponPeriods = couponPeriods + 1
        return couponPeriods
        
        
    def previewSchedule(valueDate,issueDate, maturityDate, dayCount, YTM, rate, redemValue, anni, freq, firstStub, finalStub, fv):
        couponPeriods = intScheduel.couponPeriods(issueDate,maturityDate,freq,anni,firstStub, finalStub)
        nextCouponDate = intScheduel.nextCouponDate(valueDate,maturityDate,freq,anni)
        preCouponDate = intScheduel.preCouponDate(nextCouponDate,freq)
        firstCouponDate = intScheduel.firstCouponDate(valueDate,issueDate,maturityDate,freq,anni,firstStub)
        secondFinalCouponDate = intScheduel.secondFinalCouponDate(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        isFinalPeriod = intScheduel.isFinalPeriod(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        isFirstPeriod = intScheduel.isFinalPeriod(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        finalInterest = intScheduel.finalInterest(valueDate,issueDate,maturityDate,dayCount,rate,freq,anni,finalStub)           
        firstInterest = intScheduel.firstInterest(valueDate,issueDate,maturityDate,dayCount,rate,freq,anni,firstStub)     
        
        print("Period.No", "Days", "Int.Rate", "Princ", "Int")
        for i in range(couponPeriods):
            if i == 0:
                print(i,issueDate, 0, rate, 0, 0 )
            else:
                if i == 1:
                    print(i,firstCouponDate, rate, 0, firstInterest*fv/100)
                else:
                    if i == couponPeriods-2:
                        print(i,secondFinalCouponDate, rate, 0, fv*rate/freq)
                    else:
                        if i == couponPeriods-1:
                            print(i,maturityDate, rate, redemValue*fv/100, finalInterest*fv/100)
                        else:                
                            print(i,firstCouponDate + relativedelta(months=+int(12/freq)*i) , rate, 0, fv*rate/freq)
    
    
    


# In[5]:


def yearFraction(d0,d1,dayCount,freq,anni):
    if dayCount == 1:
        return thirty_360Isda.yearFraction(d0,d1)
    if dayCount == 2:
        return thirty_360.yearFraction(d0,d1)
    if dayCount == 3:
        return thirty_360E.yearFraction(d0,d1)
    if dayCount == 4:
        return act360.yearFraction(d0,d1)
    if dayCount == 5:
        return act365.yearFraction(d0,d1)
    if dayCount == 6:
        nextCouponDate = intScheduel.nextCouponDate(d0,d1,freq,anni)
        preCouponDate = intScheduel.preCouponDate(nextCouponDate,freq)
        return actAct.yearFraction(preCouponDate,nextCouponDate,d0)
    
def daysInbetween(d0,d1,dayCount,freq,anni):
    if dayCount == 1:
        return thirty_360Isda.daysInbetween(d0,d1)
    if dayCount == 2:
        return thirty_360.daysInbetween(d0,d1)
    if dayCount == 3:
        return thirty_360E.daysInbetween(d0,d1)
    if dayCount == 4:
        return act360.daysInbetween(d0,d1)
    if dayCount == 5:
        return act365.daysInbetween(d0,d1)
    if dayCount == 6:
        nextCouponDate = intScheduel.nextCouponDate(d0,d1,freq,anni)
        preCouponDate = intScheduel.preCouponDate(nextCouponDate,freq)
        return actAct.daysInbetween(preCouponDate,nextCouponDate,d0)


# In[6]:


def testBillPrice(d0, d1, dayCount, YTM,freq,anni):
    return 100/(1+YTM*yearFraction(d0,d1,dayCount,freq,anni))


# In[7]:


class testBondPrice():  
    def cleanPrice(valueDate,issueDate, maturityDate, dayCount, YTM, rate, redemValue, anni, freq, firstStub, finalStub):
        couponPeriods = intScheduel.couponPeriods(valueDate,maturityDate,freq,anni,firstStub, finalStub)
        nextCouponDate = intScheduel.nextCouponDate(valueDate,maturityDate,freq,anni)
        preCouponDate = intScheduel.preCouponDate(nextCouponDate,freq)
        firstCouponDate = intScheduel.firstCouponDate(valueDate,issueDate,maturityDate,freq,anni,firstStub)
        secondFinalCouponDate = intScheduel.secondFinalCouponDate(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        isFinalPeriod = intScheduel.isFinalPeriod(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        isFirstPeriod = intScheduel.isFinalPeriod(valueDate,issueDate,maturityDate,freq,anni,finalStub)
        finalInterest = intScheduel.finalInterest(valueDate,issueDate,maturityDate,dayCount,rate,freq,anni,finalStub)           
        firstInterest = intScheduel.firstInterest(valueDate,issueDate,maturityDate,dayCount,rate,freq,anni,firstStub)     
        if isFinalPeriod == "true":
            dirtyPrice = (finalInterest + redemValue)*((1+YTM/freq)**(-yearFraction(valueDate,maturityDate,dayCount,freq,anni)*freq))
        else:
            if isFirstPeriod == "true":
                dirtyPrice = 0
                for i in range (couponPeriods):
                    if i == couponPeriods-1:
                        pvIntAndPrinc = ((finalInterest+redemValue)*((1+YTM/freq)**(-i+1)))*((1+YTM/freq)**(-yearFraction(secondFinalCouponDate,maturityDate,dayCount,freq,anni)*freq))
                    else:
                        pvIntAndPrinc = ((100*rate/freq)*((1+YTM/freq)**(-i)))
                    dirtyPrice = (dirtyPrice + pvIntAndPrinc)
                dirtyPrice = dirtyPrice *((1+YTM/freq)**(-yearFraction(valueDate,firstCouponDate,dayCount,freq,anni)*freq))
            else:
                dirtyPrice = 0
                for i in range (couponPeriods):
                    if i == couponPeriods-1:
                        if finalStub == "false":    
                            pvIntAndPrinc = ((finalInterest+redemValue)*((1+YTM/freq)**(-i)))
                        if finalStub == "short":
                            pvIntAndPrinc = ((finalInterest+redemValue)*((1+YTM/freq)**(-i)))/(1+YTM*yearFraction(secondFinalCouponDate,maturityDate,dayCount,freq,anni))
                        if finalStub == "long":
                            stubDate = secondFinalCouponDate + relativedelta(months=+int(12/freq))
                            pvIntAndPrinc = ((finalInterest+redemValue)*((1+YTM/freq)**(-i)))/(1+YTM*yearFraction(stubDate,maturityDate,dayCount,freq,anni))
                    else:
                        pvIntAndPrinc = ((100*rate/freq)*((1+YTM/freq)**(-i)))
                    dirtyPrice = (dirtyPrice + pvIntAndPrinc)
                dirtyPrice = dirtyPrice *((1+YTM/freq)**(-yearFraction(valueDate,nextCouponDate,dayCount,freq,anni)*freq))
        
        if dayCount == 6:
            ##Only for actActual
            accrInt = redemValue*rate/freq*(yearFraction(valueDate,maturityDate,dayCount,freq,anni))
        else:    
            accrInt = redemValue*rate*(1/freq-yearFraction(valueDate,nextCouponDate,dayCount,freq,anni))
        cleanPrice = dirtyPrice - accrInt

        return cleanPrice



    def accrInt(valueDate, maturityDate, dayCount, rate, redemValue, anni, freq):
        nextCouponDate = intScheduel.nextCouponDate(valueDate,maturityDate,freq,anni)
        preCouponDate = intScheduel.preCouponDate(nextCouponDate,freq)
        if dayCount == 6:
            ##Only for actActual
            accrInt = redemValue*rate/freq*(yearFraction(valueDate,maturityDate,dayCount,freq,anni))
        else:    
            accrInt = redemValue*rate*(1/freq-yearFraction(valueDate,nextCouponDate,dayCount,freq,anni))
        return accrInt


# In[8]:


class phpTax():
    def amort_Tax(valueDate,issueDate, maturityDate, dayCount, YTM, rate, redemValue, anni, freq, firstStub, finalStub,taxRate):
        x = testBondPrice.cleanPrice(valueDate,issueDate, maturityDate, dayCount, YTM, rate, redemValue, anni, freq, firstStub, finalStub)
        y = testBondPrice.cleanPrice(valueDate,issueDate, maturityDate, dayCount, YTM*(1-taxRate), rate*(1-taxRate), redemValue, anni, freq, firstStub, finalStub)
        return (x-y)/redemValue
    
    def wtax_Coupon(valueDate, maturityDate, dayCount, YTM, Rate, redemValue, anni, freq,taxRate):
        x = testBondPrice.accrInt(valueDate, maturityDate, dayCount, Rate, redemValue, anni, freq)*taxRate/redemValue
        return x



#next target is to pickup bond series from the data frame and make more user friendliness by buidling UI




