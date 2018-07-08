package greenHouse;

/**
 * This class is the temperature model.
 * 
 * @author yihe
 *
 */
public class TempModel {

	protected double currentTemp;
	protected double desiredTemp;
	protected double heatingRate;
	protected double coolingRate;
	protected String furnaceStatus = "";
	protected String acStatus = "";
	protected double refreshRate;

	/**
	 * This method to set the current temperature
	 * 
	 * @param currentTemp
	 *            the current temperature
	 * 
	 */
	public synchronized void setCurrentTemp(double currentTemp) {
		this.currentTemp = currentTemp;
	}

	/**
	 * This method to get the change temperature
	 * 
	 * @param deltaTemp
	 *            This is changed value of the temperature
	 */
	public synchronized void changeCurrentTemp(double deltaTemp) {
		this.currentTemp += deltaTemp;
	}

	/**
	 * This method is to get current temperature
	 * 
	 * @return current Temperature is current temperature + detla temperature
	 */
	public synchronized double getCurrentTemp() {
		return currentTemp;
	}

	/**
	 * This method is designed for user setting a value of desired temperature.
	 * 
	 * @param desiredTemp
	 *            This is user desired temperature.
	 */
	public void setDesiredTemp(double desiredTemp) {
		this.desiredTemp = desiredTemp;
	}

	/**
	 * This method will return a value of desired temperature once it is
	 * invoked.
	 * 
	 * @return desiredTemp return a temperature that user desired
	 */
	public double getDesiredTemp() {
		return desiredTemp;
	}

	/**
	 * This method sets the temperature heating rate
	 * 
	 * @param tempHeatingRate
	 *            this is the temperature heating rate
	 */

	public void setHeatingRate(double tempHeatingRate) {
		this.heatingRate = tempHeatingRate;
	}

	/**
	 * This method gets the temperature heating rate
	 * 
	 * @return temperature heating rate the value of temperature of heating rate
	 */
	public double getHeatingRate() {
		return heatingRate;
	}

	/**
	 * This method sets the temperature cooling rate
	 * 
	 * @param coolingRate
	 *            temperature cooling rate
	 */
	public void setCoolingRate(double coolingRate) {
		this.coolingRate = coolingRate;
	}

	/**
	 * This method gets the temperature cooling rate
	 * 
	 * @return temperature cooling rate the value of temperature cooling rate
	 */
	public double getCoolingRate() {
		return coolingRate;
	}

	/**
	 * The method set the refresh rate
	 * 
	 * @param setRefreshRate
	 *            how many times the program update the data
	 * 
	 */
	public void setRefreshRate(double refreshRate) {
		this.refreshRate = refreshRate;
	}

	/**
	 * The method get the value of refresh rate.
	 * 
	 * @return refreshRate a value of refresh rate to update the current
	 *         temperature and the status of temperature controller.
	 * 
	 */
	public double getRefreshRate() {
		return refreshRate;
	}

	/**
	 * This method is to set the update temperature( current temperature + heatingRate * refreshRate)
	 * 
	 */

	public synchronized void updateTemperature() {
		// We use this.getCurrentTemp() instead of this.currentTemp directly,
		// because this.getCurrentTemp() is synchronized.
		if (this.getCurrentTemp() > (desiredTemp + 3)) {
			// Subtract effective cooling rate from the temperature.
			this.changeCurrentTemp(-coolingRate * refreshRate);
		} else if (this.getCurrentTemp() < (desiredTemp - 3)) {
			// Add effective heating rate from the temperature.
			this.changeCurrentTemp(heatingRate * refreshRate);
		}
	}

	/**
	 * The method is current temperature used to compare with desired
	 * temperature and determine the status of temperature controller( air
	 * conditioner).
	 * 
	 * @return status of temperature controller(air conditioner). Once the
	 *         current temperature and desired temperature is known, the status
	 *         of air conditioner would be return.
	 * 
	 */
	public String getACStatus() {
		if (currentTemp > (desiredTemp + 3)) {
			acStatus = "AC ON";
		} else {
			acStatus = "AC OFF";
		}

		return acStatus;
	}

	/**
	 * The method is current temperature used to compare with desired
	 * temperature and determine the status of furnace.
	 * 
	 * @param currentTemp
	 *            current temperature
	 * @return status of furnace. Once the current temperature and desired
	 *         temperature is known, the status of furnace would be return.
	 */
	public String getFurnaceStatus() {
		if (currentTemp < (desiredTemp - 3)) {
			furnaceStatus = "Furnace ON";
		} else {
			furnaceStatus = "Furnace OFF";
		}
		return furnaceStatus;

	}
}
