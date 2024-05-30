package edu.gatech.seclass.jobcompare6300;

import android.content.Context;

import java.io.Serializable;
import android.util.Log;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import edu.gatech.seclass.jobcompare6300.database.OfferDetailDAO;
import edu.gatech.seclass.jobcompare6300.model.OfferDetail;
import edu.gatech.seclass.jobcompare6300.model.JobWeightSettings;
import edu.gatech.seclass.jobcompare6300.database.AdjustWeightDAO;

public class DataManager implements Serializable {

    private static OfferDetailDAO dao;
    private static AdjustWeightDAO adjustWeightDAO;

    public static final boolean DATABASE_JOB = true;
    public static final boolean DATABASE_OFFER = false;

    private static OfferDetail currentJob;
    private static List<OfferDetail> offersList;

    public DataManager(Context context) {
        dao = new OfferDetailDAO(context);

        // Get current job from db
        currentJob = dao.getCurrentJobFromDB();

        // Get offersList from db
        offersList = dao.getOffersList();

    }

    public void exitApp() {
        dao.closeDBHelper();
    }

    public static OfferDetailDAO getOfferDetailDAO() {
        return dao;
    }
    public static OfferDetail getCurrentJob() {
        return currentJob;
    }

    public static void setCurrentJob(OfferDetail job) {
        currentJob = job;
    }

    public static void addToOffersList(OfferDetail job){
        if(offersList == null){
            offersList = new ArrayList<>();
        }
        offersList.add(job);
    }

    public static List<OfferDetail> getOffersList() {
        return offersList;
    }

    /**
     * @param title Title
     * @param company Company
     * @param city City
     * @param state State
     * @param costIndex Cost of living in the location (expressed as an index)
     * @param salary Yearly salary
     * @param bonus Yearly bonus
     * @param stock Number of stock option shares offered
     * @param homeFund Home Buying Program fund (one-time dollar amount up to 15% of Yearly
     * Salary)
     * @param holiday Personal Choice Holidays (A single overall number of days from 0 to 20)
     * @param internet Monthly Internet Stipend ($0 to $75 inclusive)
     * @return the offer that is successfully added
     */
     static public OfferDetail addOffer(String title, String company, String city, String state,
                            float costIndex, float salary, float bonus, int stock, float homeFund,
                            float holiday, float internet) {

        OfferDetail offer = new OfferDetail();
        offer.setTitle(title);
        offer.setName(company);
        if (!offer.addLocation(city, state, costIndex)) return null;
        offer.setSalary(salary);
        offer.setBonus(bonus);
        offer.setStockOptions(stock);
        if (!offer.addBenefits(homeFund, holiday, internet)) return null;

        return offer;
    }

    /**
     * It is used to edit the current job.
     * @param title Title
     * @param company Company
     * @param city City
     * @param state State
     * @param costIndex Cost of living in the location (expressed as an index)
     * @param salary Yearly salary
     * @param bonus Yearly bonus
     * @param stock Number of stock option shares offered
     * @param homeFund Home Buying Program fund (one-time dollar amount up to 15% of Yearly
     * Salary)
     * @param holiday Personal Choice Holidays (A single overall number of days from 0 to 20)
     * @param internet Monthly Internet Stipend ($0 to $75 inclusive)
     * @return whether it is successfully edited
     */
    static public boolean editOffer(String title, String company, String city, String state,
                                       float costIndex, float salary, float bonus, int stock, float homeFund,
                                       float holiday, float internet) {
        OfferDetail job = DataManager.getCurrentJob();
        if (job != null) {
            job.setTitle(title);
            job.setName(company);
            if (!job.editLocation(city, state, costIndex)) {
                return false;
            }
            job.setSalary(salary);
            job.setBonus(bonus);
            job.setStockOptions(stock);
            if (!job.editBenefits(homeFund, holiday, internet)) {
                return false;
            }
            return true;
        }
        return false;
    }


}
