package greenHouse;

import java.io.PrintWriter;

/**
 * This the temperature control class
 * 
 * @author yihe
 *
 */
public class TempController extends Thread {
	private TempView tempView;
	private TempModel tempModel;
	public static PrintWriter outfile;

	/**
	 * This is class method to set the out file
	 * 
	 * @param outFile
	 *            saving file for UI on tempView
	 */
	public static void setWriter(PrintWriter outFile) {
		TempController.outfile = outFile;
	}

	/**
	 * the controller can link the TempView class and TempModel class
	 * 
	 * @param tempView
	 *            This is the class of temperature view
	 * @param tempModel
	 *            This is the class of temperature model
	 */
	public TempController(TempView tempView, TempModel tempModel) {
		this.tempView = tempView;
		this.tempModel = tempModel;
	}

	/**
	 * This the constructor for tempController
	 */
	public void run() {
		/*
		 * The only time the temperature should be SET. Any future update should
		 * use tempModel.updateTemperature(), which uses
		 * tempModel.changeCurrentTemp(). If we use SET instead of CHANGE
		 * (increment/decrement), then even if Thread2 modifies currentTemp
		 * after Thread1, it will still completely overwrite the value. With
		 * increment/decrement, Thread2 will only add/subtract from Thread1's
		 * value.
		 */
		tempModel.setCurrentTemp(stringToDouble(tempView.txtCurrentTemp.getText()));

		while (!Thread.interrupted()) {
			try {
				
				// save input to model
				tempModel.setDesiredTemp(stringToDouble(tempView.txtDesiredTemp.getText()));
				tempModel.setCoolingRate(stringToDouble(tempView.txtCoolingRate.getText()));
				tempModel.setHeatingRate(stringToDouble(tempView.txtHeatingRate.getText()));
				tempModel.setRefreshRate(stringToDouble(tempView.txtRefreshRate.getText()));

				// update Furnace/AC status
				tempView.lblFurnaceStatusValue.setText(String.format(tempModel.getFurnaceStatus()));
				tempView.lblACStatusValue.setText(String.format(tempModel.getACStatus()));

				// calculate new temperature, output to UI
				tempModel.updateTemperature();
				tempView.txtCurrentTemp.setText(Double.toString(tempModel.getCurrentTemp()));
				
				// saving the file from UI
				outfile.println(" Current Temperature: " + tempView.txtCurrentTemp.getText() + " " 
								+ " Desired Temperature: " +tempView.txtDesiredTemp.getText() + " "
								+ " Heating Rate: " + tempView.txtHeatingRate.getText() + " " 
								+ " Cooling Rate: " + tempView.txtCoolingRate.getText() + " "
								+ " Refresh Rate: " + tempView.txtRefreshRate.getText() + " "
								+ " Furnace Status: " + tempModel.getFurnaceStatus()+ " "
								+" Air Conditioner: " +tempModel.getACStatus() +" \n " );

				// wait for user-specified time interval
				Thread.sleep((int) tempModel.getRefreshRate() * 1000);

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
