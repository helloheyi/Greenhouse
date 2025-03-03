//
//  main.cpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#include <iostream>
#include "VanillaOpt.hpp"
#include "Digital_Opt.hpp"
#include "BarrierOpt.hpp"

int main()
{
    double S     = 1.35255;
    double K     = 1.357;
    double r_f   = 0.0353572370564816;
    double r_d   = 0.027921080456;
    double sigma = 0.0565554432244692;
    double T     = 2;
    double eps   = 1e-4;

    // Create a vanilla call
    VanillaOption callOption(S, K, r_d, r_f, sigma, T, OptionType::Call);
    std::cout << "Vanilla call price (million units): "
              << (callOption.Price() * 1'000'000 / S) << std::endl;

    // Vanilla put
    VanillaOption putOption(S, K, r_d, r_f, sigma, T, OptionType::Put);
    std::cout << "Vanilla put price: " << putOption.Price() << std::endl;

    // Digital call
    DigitalOption callDigital(S, K, r_d, r_f, sigma, T, OptionType::Call, eps);
    std::cout << "Digital call price (million units): "
              << (callDigital.Price() * 1'000'000) << std::endl;

    // Digital put
    DigitalOption putDigital(S, K, r_d, r_f, sigma, T, OptionType::Put, eps);
    std::cout << "Digital put price: " << putDigital.Price() << std::endl;

    // Barrier example
    double barrierLevel = 1.355;
    BarrierOption upOutCall(S, K, r_d, r_f, sigma, T, OptionType::Call,
                            barrierLevel, BarrierType::UpOut, eps);
    std::cout << "Up-and-out call price: " << upOutCall.Price() << std::endl;
}
