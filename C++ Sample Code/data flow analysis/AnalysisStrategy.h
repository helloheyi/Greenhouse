#pragma once
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/ValueMap.h"
#include "llvm/ADT/SetVector.h"
#include <string>
#include "llvm/IR/InstIterator.h"
#include "Utils.h"

using namespace llvm;

namespace dataflow{

	enum Direction { Undefined, Forward, Backward };
	enum EvalutionResult { NotApplicable = -1, Unmodified, Modified };

	/**
	 * The skeleton class for Dataflow analyses strategies
	 */
	struct AnalysisStrategy : public FunctionPass {
		public:

			/**
			 * The map of In Sets for a given Instruction.
			 * Do not add or remove the Instruction/SetVector pair or create your own SetVector*;
			 * instead, add and remove from the provided SetVector.
			 */
			ValueMap<Instruction*,SetVector<Value*>*> inMap;

			/**
			 * The map of In Sets for a given Instruction.
			 * Do not add or remove the Instruction/SetVector pair or create your own SetVector*;
			 * instead, add and remove from the provided SetVector.
			 */
			ValueMap<Instruction*,SetVector<Value*>*> outMap;

			/**
			 * AnalysisStrategy Constructor; the char ID is used in child classes by LLVM.
			 * Do not change or modify the constructor.
			*/
			AnalysisStrategy(char ID) : FunctionPass(ID) {};

			/**
			 * AnalysisStrategy Destructor
			*/
			virtual ~AnalysisStrategy() {}

			/**
			 * LLVM method that is called once for the given FunctionPass.
			 * The inMap and outMap are set up for you in this method and
			 * are available to use in your AnalysisStrategy implementations.
			*/
			bool runOnFunction(Function &F) override final;

			/**
			 * Implement your analysis in this function. Store your results in AnalysisStrategy::inMap and
			 * AnalysisStrategy:outMap.  The return result may be used by your ChaoticIterationAlgorithm
			 * as needed, but is not required to be used.  If you are going to use the result, return
			 * either Modified or Unmodified as appropriate.  If you are not using the result, return
			 * NotApplicable.
			 */
			virtual EvalutionResult evaluate(Instruction* current) = 0;

			/**
			 * Optionally to be implemented as part of the assignment
			 */
			virtual Direction getPreferredDirection() {
				return Direction::Undefined;
			}

		protected:
			virtual std::string getAnalysisName() = 0;
	};
}
