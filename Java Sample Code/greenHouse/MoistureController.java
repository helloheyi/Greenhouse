package greenHouse;

import java.io.PrintWriter;

/**
 * This is the class of moisture controller
 * 
 * @author yihe xin yin
 *
 */
public class MoistureController extends Thread {
	private MoistureView myMoiView;
	private MoistureModel myMoiModel;
	public static PrintWriter outfile;

	/**
	 * This is class method to set the out file
	 * 
	 * @param outFile
	 *            saving file for UI on MoistureView
	 */
	public static void setWriter(PrintWriter outFile) {
		MoistureController.outfile = outFile;
	}

	/**
	 * the controller can link the MoistureView class and MoistureModel class
	 * 
	 * @param myMoiView
	 *            This is the class of moisture view
	 * @param myMoiModel
	 *            This is the class of moisture model
	 */
	public MoistureController(MoistureView myMoiView, MoistureModel myMoiModel) {
		this.myMoiView = myMoiView;
		this.myMoiModel = myMoiModel;
	}

	public void run() {
		/*
		 * The only time the moisture should be SET. Any future update should
		 * use myMoiModel.updateMoisture(), which uses
		 * myMoiModel.changeCurrentMoisture(). If we use SET instead of CHANGE
		 * (increment/decrement), then even if Thread2 modifies currentMoisture
		 * after Thread1, it will still completely overwrite the value. With
		 * increment/decrement, Thread2 will only add/subtract from Thread1's
		 * value.
		 */

		myMoiModel.setCurrentSoilMoisture(stringToDouble(myMoiView.txtCurrentMoisture.getText()));

		while (!Thread.interrupted()) {
			try {
				
				// save input to model
				myMoiModel.setDesiredMaxSoilMoisture(stringToDouble(myMoiView.txtDesiredMoistureMax.getText()));
				myMoiModel.setDesiredMinSoilMoisture(stringToDouble(myMoiView.txtDesiredMoistureMin.getText()));
				myMoiModel.setSoilMoistureChangeRate(stringToDouble(myMoiView.txtMoistureRate.getText()));
				myMoiModel.setMosRefreshRate(stringToDouble(myMoiView.txtRefreshRate.getText()));

				// update sprinkler
				myMoiView.lblSprinklerStatusValue.setText(String.format(myMoiModel.getSprinklerStatus()));

				// calculate new moisture , output to UI
				myMoiModel.updateMoisture();
				myMoiView.txtCurrentMoisture.setText(Double.toString(myMoiModel.getCurrentSoilMoisture()));
				
				// saving the file from UI
				outfile.println(" Current Moisture: " +myMoiView.txtCurrentMoisture.getText() + " " 
								+ " Desired Moisture Max: " +myMoiView.txtDesiredMoistureMax.getText()+ " " 
								+ " Desired Moisture Min: "+ myMoiView.txtDesiredMoistureMin.getText() + " " 
								+ " Moisture Rate: " + myMoiView.txtMoistureRate.getText()+ " " 
								+ " Refresh Rate: " + myMoiView.txtRefreshRate.getText() + " "
								+ " Sprinkler Status: " +String.format(myMoiModel.getSprinklerStatus()) + " \n ");
				
				// wait for user-specified time interval
				Thread.sleep((int) myMoiModel.getMosRefreshRate() * 1000);
			} catch (InterruptedException e) {
				Thread.currentThread().interrupt();
			}
		}
	}

	/**
	 * Method to change String to double
	 * 
	 * @param stringToParse
	 *            This is the String Object
	 * @return double value
	 */
	public static double stringToDouble(String stringToParse) {
		return Double.parseDouble(stringToParse.trim());
	}

}