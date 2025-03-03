

// If DigitalOption were to inherit from VanillaOption, that would imply:

// A digital option is a vanilla option.

// But this isn’t correct. A digital option is fundamentally different from a vanilla option:
// It should be an independent object.

#include "Digital_Opt.hpp"
//  VanillaOption for pricing
#include "VanillaOpt.hpp"
#include <cmath>
#include <iostream>

// constructor
DigitalOption::DigitalOption(double S, double K, double r_d, double r_f, double sigma, double T, std::string Option_Type, double eps): S(S), K(K), r_d(r_d),r_f(r_f), sigma(sigma), T(T), Option_Type(Option_Type), eps(eps)
{
    
};

//
double DigitalOption::Digital_val() {
// use call/put spread method to price digital option: as a combination of a long option and a short option at different strike prices.
    std::transform(Option_Type.begin(), Option_Type.end(), Option_Type.begin(), ::tolower);
    VanillaOpt higher_strike(S, K+eps, r_d,r_f, sigma, T,Option_Type);
    VanillaOpt strike(S, K, r_d,r_f, sigma, T,Option_Type);
    
    double option_diff =  strike.option_val() - higher_strike.option_val();

    if (Option_Type == "call"){
        // define vanilla option objective
        double digital_val = option_diff/eps;
        return digital_val;
        
    }
    else if (Option_Type == "put"){
        double digital_val = (-option_diff)/eps;
        return digital_val;
    }
    else{
        std::cout << "Invalid option type!" << std::endl;
        return -1;
    }

    
}
