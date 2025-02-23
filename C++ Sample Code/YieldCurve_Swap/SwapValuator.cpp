//
//  SwapValuator.cpp
//  YieldCurve_Swap
//
//  Created by Yi He on 2024-02-19.
//

#include "SwapValuator.hpp"

SwapValuator::SwapValuator(YieldCurveBuilder& ycBuilder, double notional, double fixedRate, int frequency, int maturity,  const std::string& leg1Status)
    : ycb(ycBuilder), notional(notional), fixedRate(fixedRate), paymentFrequency(frequency), maturityDays(maturity), leg1(leg1Status)  {}
        
// value fix leg
double SwapValuator::valueFixedLeg(){
    double pv = 0.0;
    int paymentInterval =360 / paymentFrequency;
    for (int day = paymentInterval; day <= maturityDays; day += paymentInterval){
        // payment
        double payment = notional * (fixedRate / paymentFrequency);
        double df = ycb.linearInterpolate(day);
        pv += df*payment;
    }
    return pv;
}

// value float leg
double SwapValuator::valueFloatingLeg(){
    double pv = 0.0;
    int paymentInterval =360 / paymentFrequency;
    //   get the forward rates
    const std::vector<double>&forwardRates = ycb.getForwardRates(); 
    for (int day = paymentInterval, ii = 0; day <= maturityDays && ii<forwardRates.size(); day += paymentInterval, ++ii){
        double forwardRate = forwardRates[ii];
        // payment
        double payment = notional * (forwardRate/ paymentFrequency);
        double df = ycb.linearInterpolate(day);
        pv += df*payment;
    }
    return pv;
}

double SwapValuator::netSwapValue() {
    // convert leg1 to lowercase for case-insensitive comparison
    std::string leg1Lower = leg1;
    // make a copy to transform as all low char
    std::transform(leg1Lower.begin(), leg1Lower.end(), leg1Lower.begin(),[](unsigned char c){ return std::tolower(c); });
    if (leg1Lower == "long") {
        return valueFixedLeg() - valueFloatingLeg();
    } else {
        return valueFloatingLeg() - valueFixedLeg();
    }
}



