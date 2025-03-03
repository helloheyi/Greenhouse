//
//  VanillaOpt.cpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#include "VanillaOpt.hpp"
#include <algorithm>
#include <iostream>

double VanillaOption::norm_cdf(double x) const
{
    // standard normal CDF
    return 0.5 * std::erfc(-x / std::sqrt(2.0));
}

double VanillaOption::forward() const
{
    return S * std::exp((r_d - r_f) * T);
}

double VanillaOption::d1(double f) const
{
    return ( std::log(f / K) + 0.5 * sigma * sigma * T ) / ( sigma * std::sqrt(T) );
}

double VanillaOption::d2(double f) const
{
    // d2 = d1 - sigma * sqrt(T)
    return d1(f) - sigma * std::sqrt(T);
}

double VanillaOption::Price() const
{
    //  forward price for convenience
    double f = forward();
    double d1_ = d1(f);
    double d2_ = d2(f);
    double df_d = std::exp(-r_d * T);

    if (type == OptionType::Call)
    {
        return df_d * ( f * norm_cdf(d1_) - K * norm_cdf(d2_) );
    }
    else
    {
        return df_d * ( K * norm_cdf(-d2_) - f * norm_cdf(-d1_) );
    }
}
