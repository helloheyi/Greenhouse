//
//  YieldCurveBuilder.cpp
//  YieldCurve_Swap
//
//  Created by Yi He on 2024-02-19.
//
#include "YieldCurveBuilder.hpp"

YieldCurveBuilder::YieldCurveBuilder(const std::vector<MarketQuote>& inputQuotes) : quotes(inputQuotes) {
}

double YieldCurveBuilder::linearInterpolate(int day) {
    if (quotes.empty()) return 1.0;
    for (size_t i = 0; i < quotes.size() - 1; ++i) {
        
        if (day >= quotes[i].days && day <= quotes[i + 1].days){
            double x0 = quotes[i].days;
            double y0 = discountFactors[i];
            double x1 = quotes[i + 1].days;
            double y1 = discountFactors[i + 1];
            return y0 + (day - x0) * (y1 - y0) / (x1 - x0);
        }
    }
    
    
    return 1.0 ;
}

void YieldCurveBuilder::bootstrapDiscountFactors() {
    discountFactors.resize(quotes.size(), 0.0);
    int firstDay = quotes[0].days;
    double firstRate = quotes[0].rate;
    discountFactors[0] = 1.0 / (1.0 + firstRate * firstDay / 360.0);
    
    for (size_t ii = 1; ii < quotes.size(); ++ii) {
        int currentDay = quotes[ii].days;
        double currentRate = quotes[ii].rate;
        int lastDay = quotes[ii - 1].days;
        int dayDelta = currentDay - lastDay;
        discountFactors[ii] = discountFactors[ii - 1] / (1.0 + currentRate * dayDelta / 360.0);
    }
}



void YieldCurveBuilder::calculateForwardRates() {    
    forwardRates.resize(quotes.size() -1 , 0.0);
    for (size_t ii = 0; ii < quotes.size() - 1; ++ii) {
        double D1 = discountFactors[ii];
        double D2 = discountFactors[ii+1];
        int T1 = quotes[ii].days;
        int T2 = quotes[ii + 1].days;
        forwardRates[ii] = ((1 / D2) - (1 / D1)) / (D1 * (T2 - T1)) * 360;
        
    }
    
}

const std::vector<double>& YieldCurveBuilder::getDiscountFactors() const{
    return discountFactors;
}
const std::vector<double>& YieldCurveBuilder::getForwardRates() const{
    return forwardRates;
};
