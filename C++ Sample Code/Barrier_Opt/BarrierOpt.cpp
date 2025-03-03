#include "BarrierOpt.hpp"
#include "VanillaOpt.hpp"
#include "Digital_Opt.hpp"
#include <iostream>
// constructor
BarrierOpt:: BarrierOpt(double S, double K, double r_d, double r_f, double sigma, double T, double eps,double B,std::string Option_Type,std::string Knock_Type): S(S), K(K), r_d(r_d), r_f(r_f), sigma(sigma), T(T),eps(0.0001),B(B), Option_Type(Option_Type), Knock_Type(Knock_Type)
{
    
    
}
// determine knock Type
int BarrierOpt::knockTypeAsInt() const{
    if (Knock_Type == "up_out")    return 1;
    if (Knock_Type == "down_out")  return 2;
    if (Knock_Type == "up_in")   return 3;
    if (Knock_Type == "down_in")     return 4;
    return 0; // unknown
}


// call type
double BarrierOpt::Barrier_call() const{
//    std::transform(Knock_Type.begin(), Knock_Type.end(), Knock_Type.begin(), ::tolower);
    int typeval = knockTypeAsInt();
    VanillaOpt vanilla_K(S, K, r_d,r_f, sigma,T, "Call");
    VanillaOpt vanilla_B(S, B, r_d,r_f, sigma,T, "Call");
    DigitalOption digital_B(S, B, r_d,r_f, sigma,T, "Call",0.0001);

    if (K>=B){
        
        switch(typeval)
        {
            case 1:
                return 0;
            case 2:
            
                return vanilla_K.option_val();
            case 3:
            
                return vanilla_K.option_val();
            case 4:
                return 0;
            default:
                std::cout <<"Invalid Knock Type"<< std::endl;
                return -1;
        }
    }
        else{
            switch(typeval)
            {
                case 1:
                
                    return vanilla_K.option_val() -vanilla_B.option_val() - (B-K)*digital_B.Digital_val();
                
                case 2:
               
                    return vanilla_B.option_val() +(B-K)*digital_B.Digital_val();
                case 3:
                
                    return vanilla_B.option_val() +(B-K)*digital_B.Digital_val();
                case 4:
                    return vanilla_K.option_val() -vanilla_B.option_val() - (B-K)*digital_B.Digital_val();
                default:
                    std::cout <<"Invalid Knock Type"<< std::endl;
                    return -1;
            }
        }
}

// put type
double BarrierOpt::Barrier_put() const{
    
//    std::transform(Knock_Type.begin(), Knock_Type.end(), Knock_Type.begin(), ::tolower);
    int typeval = knockTypeAsInt();
    VanillaOpt vanilla_K(S, K, r_d, r_f, sigma,T, "put");
    VanillaOpt vanilla_B(S, B, r_d, r_f, sigma,T, "put");
    DigitalOption digital_B(S, B, r_d, r_f, sigma,T, "put",0.0001);
    
    if (K<=B){
        
        switch(typeval)
        {
            case 1:
                return vanilla_K.option_val();
            case 2:
                
                return 0;
            case 3:
                
                return 0;
            case 4:
                return vanilla_K.option_val();
            default:
                std::cout <<"Invalid Knock Type"<< std::endl;
                return -1;
        }
    }
    else{
        switch(typeval)
        {
            case 1:
                
                return vanilla_B.option_val() +(B-K)*digital_B.Digital_val();
                
            case 2:
                
                return  vanilla_K.option_val() -vanilla_B.option_val() - (B-K)*digital_B.Digital_val();
            case 3:
                
                return vanilla_K.option_val() -vanilla_B.option_val() - (B-K)*digital_B.Digital_val();
            case 4:
                return vanilla_B.option_val() +(B-K)*digital_B.Digital_val();
            default:
                std::cout <<"Invalid Knock Type"<< std::endl;
                return -1;
        }
    }
    
    
}
double BarrierOpt::Barrier_val(){
    std::transform(Option_Type.begin(), Option_Type.end(),Option_Type.begin(), ::tolower);
    std::transform(Knock_Type.begin(), Knock_Type.end(), Knock_Type.begin(), ::tolower);
    if (Option_Type == "call"){
        return Barrier_call();
    }
    else if (Option_Type == "put"){
        
        return Barrier_put();
    }
    else{
        std::cout << "Invalid option type!" << std::endl;
        return -1;
    }
};

