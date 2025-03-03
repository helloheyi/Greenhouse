//
//  Digital_Opt.cpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#include "Digital_Opt.hpp"
#include "VanillaOpt.hpp"


double DigitalOption::Price() const
{
    // difference of two vanilla calls/puts
    // with strikes K and K+eps.

    double Kplus = K + eps;

    VanillaOption vanillaK(     S, K,      r_d, r_f, sigma, T, type );
    VanillaOption vanillaKplus( S, Kplus,  r_d, r_f, sigma, T, type );

    double diff = vanillaK.Price() - vanillaKplus.Price();

    if (type == OptionType::Call)
    {
        // call
        // digital = (C(K) - C(K+eps)) / eps
        return diff / eps;
    }
    else
    {   // put
        // digital = (P(K+eps) - P(K)) / eps
        // which is the same as -(diff)/eps if we define diff = P(K)-P(K+eps).
        return -diff / eps;
    }
}
