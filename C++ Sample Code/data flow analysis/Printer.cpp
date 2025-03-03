
#include "Utils.h"

namespace dataflow{
	struct Printer: public FunctionPass {
		static char ID;
		Printer() : FunctionPass(ID){}
		
	protected:

		/**
	 	 * Print information about each instruction in each function. 
		 */
		bool runOnFunction(Function &F) override {
			errs() << "Print information about instructions in " << F.getName() << "\n";
			for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I){
				errs() << "Instruction: " << *I << "\n"; 
				errs() << "Def set: [";
				if (isDef(&(*I))){
					errs() << *I;	
				} 	
				errs() << "]\n";
				errs() << "Use set: [";
				// Get values used in the instruction.
				for (Use& U : I->operands()){
					Value* v = U.get();
					// Check if Value v is a local variable.
					if(isa<Instruction>(v))
						errs() << *v << ", ";
				}	
				errs() << "]\n";
				errs() << "Predecessors: [";
				for(Instruction* P : getPredecessors(&(*I))) 
					errs() << *P << ", ";
				errs() << "]\n";
				errs() << "Successors: [";
				for(Instruction* S : getSuccessors(&(*I)))
					errs() << *S << ", ";
				errs() << "]\n\n";
			}
			return false;
		}
	};
	
	char Printer::ID = 2;
	static RegisterPass<Printer> X("Printer", "Print information about instructions in each function.",
											false /* Only looks at CFG */,
											false /* Analysis Pass */);
}
