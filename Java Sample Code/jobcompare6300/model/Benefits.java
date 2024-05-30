package edu.gatech.seclass.jobcompare6300.model;

import java.io.Serializable;

public class Benefits implements Serializable {
    private float homeProgramFund;
    private float holidays;
    private float internetStipend;

    public float getHomeProgramFund() {
        return homeProgramFund;
    }

    public void setHomeProgramFund(float homeProgramFund) {
        this.homeProgramFund = homeProgramFund;
    }

    public float getHolidays() {
        return holidays;
    }

    public void setHolidays(float holidays) {
        this.holidays = holidays;
    }

    public float getInternetStipend() {
        return internetStipend;
    }

    public void setInternetStipend(float internetStipend) {
        this.internetStipend = internetStipend;
    }
}