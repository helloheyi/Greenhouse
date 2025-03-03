
#ifndef Digital_Opt_hpp
#define Digital_Opt_hpp

#include <string>
#include <stdio.h>
class DigitalOption {
    // inside Class only
    private:
    // option parameters
        double S;
        double K;
        double r_d;
        double r_f;
        double sigma;
        double T;
        std::string Option_Type;
        double eps;
    
    public:
    // can be access outside class for valuation
    //constructor
    DigitalOption(double S, double K, double r_d, double r_f, double sigma, double T, std::string Option_Type,double eps);
    // deconstructor to cleanup resources if required
    // ~DigitalOption();
    double Digital_val();
    
};
#endif /* Digital_Opt_hpp */
