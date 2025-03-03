

#include "VanillaOpt.hpp"
#include "VanillaOpt.hpp"
#include <cmath>
#include <string>
#include <iostream>

// constructor
VanillaOpt::VanillaOpt(double S, double K, double r_d,double r_f, double sigma, double T, std::string Option_Type)
    : S(S), K(K), r_d(r_d), r_f(r_f), sigma(sigma), T(T), Option_Type(Option_Type)
{
}

//const function does not modify any member variables of the class.
// does not modify any member variables of the class.
// norm_cdf
double VanillaOpt::norm_cdf(double x) const
{
//    const double pi = 3.141592653589793;
//    return 1/std::sqrt(2*pi) * std::exp(-(x*x)/2);
    return 0.5 * std::erfc(-x / std::sqrt(2.0));

}
// conver to forward

double VanillaOpt::forward()const{
    
    return S*std::exp((r_d - r_f)*T);
    
}
// d1
double VanillaOpt:: d1(double f) const{
        
        return (std::log(f/K) + (sigma*sigma*0.5)*T)/(sigma* std::sqrt(T));
}

// d2
double VanillaOpt:: d2(double f) const{
    
    return d1(f) - sigma*std::sqrt(T);
}

// value option
double VanillaOpt:: option_val() {
    // insensitivity of option type, convert to lowercase
//    std::string lowerType = Option_Type;  // make a local copy
    std::transform(Option_Type.begin(), Option_Type.end(), Option_Type.begin(), ::tolower);
    double f = forward();
    double d1_ = d1(f);
    double d2_ = d2(f);
    double df_d = std::exp((-r_d)*T);

    if (Option_Type == "call"){
        
        // discount factor
        return df_d *(f*norm_cdf(d1_) - K*norm_cdf(d2_));
        
    }
    else if (Option_Type == "put"){
        //return df_d *( K*norm_cdf(-d2_) - f*norm_cdf(d1_));
        return df_d *( K*norm_cdf(-d2_) - f*norm_cdf(-d1_));
    }
    else{
        std::cout << "Invalid option type!" << std::endl;
        return -1;
    }
   
}
