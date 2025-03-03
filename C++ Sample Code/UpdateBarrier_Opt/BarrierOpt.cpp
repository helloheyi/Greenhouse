//
//  BarrierOpt.cpp
//  UpdateBarrier_Opt
//
//  Created by Yi He on 2025-03-02.
//

#include "BarrierOpt.hpp"
#include "VanillaOpt.hpp"
#include "Digital_Opt.hpp"
#include <iostream>


double BarrierOption::BarrierCall() const
{
    // vanilla & digital
    VanillaOption vanillaK(S, K, r_d, r_f, sigma, T, OptionType::Call);
    VanillaOption vanillaB(S, B, r_d, r_f, sigma, T, OptionType::Call);
    DigitalOption digitalB(S, B, r_d, r_f, sigma, T, OptionType::Call, eps);

    // K >= B
    if (K >= B)
    {
        // check barrier type:
        if (bType == BarrierType::UpOut)
        {
            return 0.0;
        }
        else if (bType == BarrierType::DownOut)
        {
            return vanillaK.Price();
        }
        else if (bType == BarrierType::UpIn)
        {
            return vanillaK.Price();
        }
        else if (bType == BarrierType::DownIn)
        {
            return 0.0;
        }
        else
        {
            std::cerr << "Invalid barrier type.\n";
            return -1.0;
        }
    }
    // K < B
    else
    {
        if (bType == BarrierType::UpOut)
        {
            return vanillaK.Price()
                - vanillaB.Price()
                - (B - K) * digitalB.Price();
        }
        else if (bType == BarrierType::DownOut)
        {
            return vanillaB.Price()
                + (B - K) * digitalB.Price();
        }
        else if (bType == BarrierType::UpIn)
        {
            return vanillaB.Price()
                + (B - K) * digitalB.Price();
        }
        else if (bType == BarrierType::DownIn)
        {
            return vanillaK.Price()
                - vanillaB.Price()
                - (B - K) * digitalB.Price();
        }
        else
        {
            std::cerr << "Invalid barrier type.\n";
            return -1.0;
        }
    }
}

double BarrierOption::BarrierPut() const
{
    // vanilla & digital
    VanillaOption vanillaK(S, K, r_d, r_f, sigma, T, OptionType::Put);
    VanillaOption vanillaB(S, B, r_d, r_f, sigma, T, OptionType::Put);
    DigitalOption digitalB(S, B, r_d, r_f, sigma, T, OptionType::Put, eps);

    // K <= B
    if (K <= B)
    {
        if (bType == BarrierType::UpOut)
        {
            return vanillaK.Price();
        }
        else if (bType == BarrierType::DownOut)
        {
            return 0.0;
        }
        else if (bType == BarrierType::UpIn)
        {
            return 0.0;
        }
        else if (bType == BarrierType::DownIn)
        {
            return vanillaK.Price();
        }
        else
        {
            std::cerr << "Invalid barrier type.\n";
            return -1.0;
        }
    }
    //  K > B
    else
    {
        if (bType == BarrierType::UpOut)
        {
            return vanillaB.Price()
                + (B - K) * digitalB.Price();
        }
        else if (bType == BarrierType::DownOut)
        {
            return vanillaK.Price()
                - vanillaB.Price()
                - (B - K) * digitalB.Price();
        }
        else if (bType == BarrierType::UpIn)
        {
            return vanillaK.Price()
                - vanillaB.Price()
                - (B - K) * digitalB.Price();
        }
        else if (bType == BarrierType::DownIn)
        {
            return vanillaB.Price()
                + (B - K) * digitalB.Price();
        }
        else
        {
            std::cerr << "Invalid barrier type.\n";
            return -1.0;
        }
    }
}

double BarrierOption::Price() const
{
    //  BarrierCall or BarrierPut
    if (type == OptionType::Call) {
        return BarrierCall();
    } else {
        return BarrierPut();
    }
}

//int BarrierOption::knockTypeAsInt() const
//{
//    if (bType == BarrierType::UpOut)   return 1;
//    if (bType == BarrierType::DownOut) return 2;
//    if (bType == BarrierType::UpIn)    return 3;
//    if (bType == BarrierType::DownIn)  return 4;
//    // unknown
//    return 0;
//    
//}


//double BarrierOption::BarrierCall() const
//{
//   
//    // vanilla & digital
//    VanillaOption vanillaK( S, K, r_d, r_f, sigma, T, OptionType::Call );
//    VanillaOption vanillaB( S, B, r_d, r_f, sigma, T, OptionType::Call );
//    DigitalOption digitalB( S, B, r_d, r_f, sigma, T, OptionType::Call, eps );
//    int bt = knockTypeAsInt();
//    // match your prior logic about if K >= B, etc.
//    if (K >= B)
//    {
//        switch(bt)
//        {
//        case 1: // up_out
//            return 0;
//        case 2: // down_out
//            return vanillaK.Price();
//        case 3: // up_in
//            return vanillaK.Price();
//        case 4: // down_in
//            return 0;
//        default:
//            std::cerr << "Invalid barrier type.\n";
//            return -1;
//        }
//    }
//    else
//    {
//        switch(bt)
//        {
//        case 1: 
//                // up_out
//            // call up-out with K < B => vanillaK - vanillaB - (B-K)*digitalB
//            return vanillaK.Price() - vanillaB.Price() - (B - K) * digitalB.Price();
//        case 2: 
//                // down_out
//            return vanillaB.Price() + (B - K)* digitalB.Price();
//        case 3: 
//                // up_in
//            return vanillaB.Price() + (B - K)* digitalB.Price();
//        case 4: 
//                // down_in
//            return vanillaK.Price() - vanillaB.Price() - (B - K)* digitalB.Price();
//        default:
//            std::cerr << "Invalid barrier type.\n";
//            return -1.0;
//        }
//    }
//}
//
//double BarrierOption::BarrierPut() const
//{
//    
//     //  vanilla & digital
//     VanillaOption vanillaK( S, K, r_d, r_f, sigma, T, OptionType::Put );
//     VanillaOption vanillaB( S, B, r_d, r_f, sigma, T, OptionType::Put );
//     DigitalOption digitalB( S, B, r_d, r_f, sigma, T, OptionType::Put, eps );
//     int bt = knockTypeAsInt();
//     // match your prior logic about if K >= B, etc.
//     if (K <= B)
//     {
//         switch(bt)
//         {
//         case 1: // up_out
//             return vanillaK.Price();
//         case 2: // down_out
//             return 0;
//         case 3: // up_in
//               return 0;
//         case 4: // down_in
//              return vanillaK.Price();
//         default:
//             std::cerr << "Invalid barrier type.\n";
//             return -1;
//         }
//     }
//     else
//     {
//         switch(bt)
//         {
//         case 1:
//                 // up_out
//             // call up-out with K < B => vanillaK - vanillaB - (B-K)*digitalB
//                 return vanillaB.Price() + (B - K)* digitalB.Price();
//                 
//         case 2:
//                 // down_out
//                 return vanillaK.Price() - vanillaB.Price() - (B - K) * digitalB.Price();
//         case 3:
//                 // up_in
//                 return vanillaK.Price() - vanillaB.Price() - (B - K) * digitalB.Price();
//         case 4:
//                 // down_in
//                 return vanillaB.Price() + (B - K)* digitalB.Price();
//         default:
//             std::cerr << "Invalid barrier type.\n";
//             return -1;
//         }
//     }
//}

