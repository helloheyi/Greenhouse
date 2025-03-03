
#pragma once
#include "llvm/IR/Function.h"
#include "AnalysisStrategy.h"

using namespace llvm;

namespace dataflow {
	struct IChaoticIterationAlgorithm {
		public:
			IChaoticIterationAlgorithm() {}
			~IChaoticIterationAlgorithm() {}
			virtual void Run(AnalysisStrategy* analysisStrategy, Function &F) = 0;
	};
}
