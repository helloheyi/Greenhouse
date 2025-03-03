
#include "AnalysisStrategy.h"
#include "IChaoticIterationAlgorithm.h"
#include <vector>
#include <algorithm>
#include <random>
#include "llvm/IR/Instructions.h"

namespace dataflow {
	struct ChaoticIterationAlgorithm : public IChaoticIterationAlgorithm {
		void Run(AnalysisStrategy* analysisStrategy, Function &F) {
            std::vector<Instruction*> instructions;
            for (auto& B : F) {
                    for (auto& I : B) {
                        instructions.push_back(&I);
                    }
                }
            
            bool hasChanged = true;
            std::random_device rd;
            std::mt19937 g(rd());

            // convergent
            while (hasChanged) {
                hasChanged = false;
                
                // shuffle the instructions chaotically
                std::shuffle(instructions.begin(), instructions.end(), g);
                
                // process each instruction in random order
                for (Instruction* I : instructions) {
                    // comparison
                    SetVector<Value*>* oldInSet = analysisStrategy->inMap[I];
                    SetVector<Value*>* oldOutSet = analysisStrategy->outMap[I];
                    auto result = analysisStrategy->evaluate(I);
                   
                    if (result == EvalutionResult::Modified) {
                        hasChanged = true;
                    }
                }
            }
		}
	};
}
