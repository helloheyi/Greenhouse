//
//  SwapValuator.hpp
//  YieldCurve_Swap
//
//  Created by Yi He on 2024-02-19.
//

#ifndef SwapValuator_hpp
#define SwapValuator_hpp

#include "YieldCurveBuilder.hpp"
#include <iostream>
#include <vector>
#include <cmath>
#include <string>

class SwapValuator {
public:
    SwapValuator(YieldCurveBuilder& ycBuilder, double notional, double fixedRate, int frequency, int maturity, const std::string& leg1Status);
    virtual ~SwapValuator(){};
    double valueFixedLeg();
    double valueFloatingLeg();
    double netSwapValue();

private:
    YieldCurveBuilder& ycb;
    double notional;
    double fixedRate;
    int paymentFrequency;
    int maturityDays;
    std::string leg1;
};
#endif /* SwapValuator_hpp */
