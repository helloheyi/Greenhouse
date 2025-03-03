

#include <iostream>
#include "VanillaOpt.hpp"
#include "Digital_Opt.hpp"
#include "BarrierOpt.hpp"

int main()
{
    double S     = 1.35255;
    double K     = 1.357;
    //double r_d   = 0.0279125259633011;
    double r_f   = 0.0353572370564816;
    double r_d   = 0.027921080456;
    //double r_f   = 0.035353530446;
    
    //    double sigma = 0.055;
    double sigma = 0.0565554432244692;
    double T     = 2;
    double epsilon = 0.0001;
    
    
    std::string call = "CAll";
    std::string put = "put";
    
    //  a Call option
    VanillaOpt callOption(S, K, r_d,r_f, sigma, T, call);
//    double call_val =callOption.option_val();
//    double res =call_val *1000000 /S;
    
    std::cout << "Call option price: " << (callOption.option_val()*1000000 /S) << std::endl;
    
    // a Put option
    VanillaOpt putOption(S, K, r_d,r_f, sigma, T, put);
    std::cout << "Put option price: " << putOption.option_val() << std::endl;
    
    
    DigitalOption call_digitalOption(S, K, r_d,r_f, sigma, T, call,epsilon);
    
    std::cout << "Digital Call Price: " << (call_digitalOption.Digital_val()*1000000) << std::endl;
    DigitalOption put_digitalOption(S, K, r_d,r_f, sigma, T, put,epsilon);
    
    std::cout << "Digital Put Price:  " << put_digitalOption.Digital_val()  << std::endl;
    
    double K_UO_B = 1.355;
    double B_UO_B = 1.357;
    BarrierOpt UO_B(S, K_UO_B, r_d,r_f, sigma, T,epsilon, B_UO_B, call,"UP_out");
    std::cout << "Barrier UO Price given K < B: " << UO_B.Barrier_val() << std::endl;
    
    double K_UO_K = 1.358;
    double B_UO_K = 1.355;
    BarrierOpt UO_K(S, K_UO_K, r_d,r_f, sigma, T,epsilon, B_UO_K, call,"UP_out");
    std::cout << "Barrier UO Price given K > B:  " << UO_K.Barrier_val()  << std::endl;
    
    
}
