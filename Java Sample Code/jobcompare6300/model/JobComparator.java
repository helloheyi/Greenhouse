package edu.gatech.seclass.jobcompare6300.model;

import edu.gatech.seclass.jobcompare6300.model.OfferDetail;

public class JobComparator implements java.util.Comparator<OfferDetail> {

    private float AYS;
    private float AYB;
    private float CSO;
    private float HBP;
    private float PCH;
    private float MIS;

    public  JobComparator(float AYS, float AYB, float CSO, float HBP, float PCH, float MIS) {
        this.AYS = AYS;
        this.AYB = AYB;
        this.CSO = CSO;
        this.HBP = HBP;
        this.PCH = PCH;
        this.MIS = MIS;
    }

    @Override
    public int compare(OfferDetail a, OfferDetail b) {
        float s1 = (this.AYS * a.getSalary() + this.AYB * a.getBonus()) / a.getLocation().costOfLiving * 100 +
                (this.CSO * (float) a.getStockOptions() / 3) + this.HBP * a.getBenefits().getHomeProgramFund() +
                (this.PCH * a.getBenefits().getHolidays() * a.getSalary() / a.getLocation().costOfLiving * 100
                        / 260) + (this.MIS * a.getBenefits().getInternetStipend() * 12);
        float s2 = (this.AYS * b.getSalary() + this.AYB * b.getBonus()) / b.getLocation().costOfLiving * 100 +
                (this.CSO * (float) b.getStockOptions() / 3) + this.HBP * b.getBenefits().getHomeProgramFund() +
                (this.PCH * b.getBenefits().getHolidays() * b.getSalary() / b.getLocation().costOfLiving * 100
                        / 260) + (this.MIS * b.getBenefits().getInternetStipend() * 12);

        return -Float.compare(s1, s2);
    }
}