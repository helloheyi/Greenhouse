package greenHouse;

import java.io.PrintWriter;

/**
 * The class is the humidity controller
 * 
 * @author yihe 
 *
 */

public class HumidityController extends Thread {
	private HumidityView humidityView;
	private HumidityModel humidityModel;
	public static PrintWriter outfile;

	/**
	 * This is class method to set the out file
	 * 
	 * @param outFile
	 *            saving file for UI on HumidityView
	 */
	public static void setWriter(PrintWriter outFile) {
		HumidityController.outfile = outFile;
	}

	/**
	 * the controller can link the HumidityView class and HumidityModel class
	 * 
	 * @param humidityView
	 *            This is the class of humidity view
	 * @param humidityModel
	 *            This is the class of humidity model
	 */
	public HumidityController(HumidityView humidityView, HumidityModel humidityModel) {
		this.humidityView = humidityView;
		this.humidityModel = humidityModel;
	}

	public void run() {
		/*
		 * The only time the humidity should be SET. Any future update should
		 * use humidityModel.updateHumidity(), which uses
		 * humidityModel.changeCurrentHumidity(). If we use SET instead of
		 * CHANGE (increment/decrement), then even if Thread2 modifies
		 * currentHumidity after Thread1, it will still completely overwrite the
		 * value. With increment/decrement, Thread2 will only add/subtract from
		 * Thread1's value.
		 */

		humidityModel.setCurrentHumidity(stringToDouble(humidityView.txtCurrentHumidity.getText()));
		while (!Thread.interrupted()) {
			try {

				// save input to model
				humidityModel.setDesiredHumidityMax(stringToDouble(humidityView.txtDesiredHumidityMax.getText()));
				humidityModel.setDesiredHumidityMin(stringToDouble(humidityView.txtDesiredHumidityMin.getText()));
				humidityModel.setHumidityRate(stringToDouble(humidityView.txtHumidityRate.getText()));
				humidityModel.setRefreshRate(stringToDouble(humidityView.txtRefreshRate.getText()));

				// update humidifer status
				humidityView.lblHumidifierStatusValue.setText(String.format(humidityModel.getHumidiferStatus()));

				// calculate new humidity , output to UI
				humidityModel.updateHumidity();
				humidityView.txtCurrentHumidity.setText(Double.toString(humidityModel.getCurrentHumidity()));

				// saving the file from UI
				outfile.println(" Current Humidity: "+humidityView.txtCurrentHumidity.getText() + " "
						+" Desired Humidity Max: "+ humidityView.txtDesiredHumidityMax.getText() + " "
						+ " Desired Humidity Min: "+humidityView.txtDesiredHumidityMin.getText() + " " 
						+ " Humidity Rate: "+humidityView.txtHumidityRate.getText()+ " " 
						+ " Retfreash Rate: "+humidityView.txtRefreshRate.getText() + " " 
						+ " Humidifer Status: "+humidityModel.getHumidiferStatus() + " \n ");

				// wait for user-specified time interval
				this.sleep((int) humidityModel.getRefreshRate() * 1000);
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
		return Double.parseDouble(stringToParse);
	}

}
